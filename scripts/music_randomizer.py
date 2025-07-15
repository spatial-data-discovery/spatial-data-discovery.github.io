#!/usr/bin/env python3
#
# music_randomizer.py
#
##############################################################################
# REQUIRED MODULES
##############################################################################
import argparse
import errno
import hashlib
import os
import random
import re
import shutil
import sqlite3

from tinytag import TinyTag
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.id3 import APIC # Album Art
from mutagen.id3 import TPE1 # Artist
from mutagen.id3 import TALB # Album
from mutagen.id3 import TDRC # Year
from mutagen.id3 import error


##############################################################################
# DOCUMENTATION
##############################################################################
__doc__ = """
MusicMan Module

Tired of your audio system's random or shuffle playing the same songs over
and over again? This module provides the MusicMan class, a utility designed to
organize and manage MP3 audio files, primarily for playback on USB-enabled
car audio systems or similar devices that support a flat folder structure
and randomized filenames.

The MusicMan class automates the process of:

1.  Discovering all MP3 files within a specified base directory and its
    subdirectories.
2.  Renaming files with a random numerical prefix (e.g., "0001. Title.mp3")
    to facilitate randomized playback on devices that sort by filename.
3.  Distributing these renamed files into a series of numbered sub-folders
    (e.g., "folder-01/", "folder-02/") to comply with typical device limitations
    on the number of files per folder or total folders.
4.  Moving the files from their original locations to these new organized
    folders.
5.  Cleaning up any empty directories left behind after the move operation.
6.  Building and maintaining a persistent SQLite database that stores metadata
    (Artist, Title, Album, etc.) for all processed songs, along with their
    original and current file paths. This database allows for efficient
    querying of the music collection without needing to re-scan all files.
    Problematic files with missing or unreadable metadata are reported and
    excluded from the database to maintain data integrity.
7.  Providing a method to query the stored music metadata and display
    the results in a human-readable Markdown table format.

The primary use case is to prepare a large, potentially disorganized, music
collection for seamless playback on car stereos that lack advanced Browse
features but support basic folder navigation and filename-based sorting.

Example Usage:
    >>> from music_randomizer import MusicMan
    >>> base_directory = "/path/to/your/music_library"
    >>> mm = MusicMan(base_directory)

    # Shuffle your MP3 library (builds a database for querying)
    >>> mm.run()

    # Query the new music collection
    >>> results = mm.query_music("artist", "Beatles")
    >>> mm.print_query_results_markdown(results, "artist", "Beatles")

    >>> results_by_title = mm.query_music("title", "Love")
    >>> mm.print_query_results_markdown(results_by_title, "title", "Love")

Version:
    0.4

Last Edited:
    2025-07-15

Author:
    Tyler W. Davis

"""
__all__ = [
    "MusicMan"
]


##############################################################################
# CLASSES
##############################################################################
class MusicMan(object):
    """Class for randomizing and organizing MP3 files for USB playback.

    Notes:
        History:
            Version 0.4:
                -   create SQLite3 database for querying songs
            Version 0.3.2:
                -   added argparse; rm show_help [20.02.02]
            Version 0.3:
                -   updated rename mp3 files function [17.01.15]
            Version 0.2:

            Version 0.4:
                -   create SQLite3 database for querying songs
                -   update find files to skip hidden folders
            Version 0.3.2:
                -   added argparse; rm show_help [20.02.02]
            Version 0.3:
                -   updated rename mp3 files function [17.01.15]
            Version 0.2:
                -   use Reader class for mp3 title tag in file remaining
                    [17.01.14]
    """
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Class Parameters
    # ////////////////////////////////////////////////////////////////////////
    DB_FILE = ".musicman.db"     # hidden SQLite3 database file
    MAX_SONGS = 130560           # Denon: 999; Subaru: 130560
    MAX_SONGS_PER_FOLDER = 25
    MAX_FOLDERS = 512

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Class Initialization
    # ////////////////////////////////////////////////////////////////////////
    def __init__(self, base_dir):
        """
        Name:     MusicMan.__init__
        Inputs:   str, base directory (base_dir)
        Features: Initializes the MusicMan class
        """
        # Initialize class variables:
        self.file_list = []
        self.file_dict = {}

        if os.path.isdir(base_dir):
            self.base_dir = base_dir
        else:
            self.base_dir = None
            raise OSError("Directory '%s' does not exist" % (base_dir))

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Class Property Definitions
    # ////////////////////////////////////////////////////////////////////////
    @property
    def num_files(self):
        return len(self.file_list)

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Class Function Definitions
    # ////////////////////////////////////////////////////////////////////////
    def _generate_song_fingerprint(self, title, artist, album, duration_seconds):
        """
        Generate a consistent hash for a song based on its core metadata.
        Handles None values gracefully by representing their absence in the hash.
        """
        # Convert None to specific string representations for hashing consistency
        _title = title if title is not None else "[NO_TITLE]"
        _artist = artist if artist is not None else "[NO_ARTIST]"
        _album = album if album is not None else "[NO_ALBUM]"
        _duration = duration_seconds if duration_seconds is not None else 0.0 # Duration should always be a number

        data = f"{_artist}|{_album}|{_title}|{_duration}"
        return hashlib.md5(data.lower().strip().encode('utf-8')).hexdigest()

    def _build_metadata_db(self):
        """
        Build or update the SQLite database with music metadata
        after files have been moved and organized.
        """
        db_path = os.path.join(self.base_dir, self.DB_FILE)
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS songs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    song_fingerprint TEXT UNIQUE NOT NULL, -- Our stable identifier
                    original_path TEXT NOT NULL,
                    current_folder_path TEXT NOT NULL,
                    current_filename TEXT NOT NULL,
                    title TEXT,
                    artist TEXT,
                    album TEXT,
                    genre TEXT,
                    year INTEGER,
                    duration_seconds REAL,
                    file_size_bytes INTEGER,
                    last_modified_timestamp REAL
                );
            """)

            # Store fingerprints of songs processed in this run to detect deletions later
            processed_fingerprints_this_run = set()
            critical_metadata_missing_count = 0

            # Iterate through the file_dict, which now has the final paths
            for new_file_name_key, (original_path_from_dict, new_full_path) in self.file_dict.items():
                if not new_full_path:
                    print(f"Warning: Missing new_full_path for {new_file_name_key}. Skipping metadata extraction.")
                    continue

                if not os.path.exists(new_full_path):
                    print(f"Warning: File not found at {new_full_path} during DB build. Skipping metadata extraction.")
                    continue

                current_folder_path = os.path.dirname(new_full_path)

                # Initialize variables to None/0.0 as we will check for their
                # presence
                title, artist, album, genre, year = None, None, None, None, None
                duration, file_size, last_modified = None, None, None

                try:
                    tag = TinyTag.get(new_full_path)
                    title = tag.title
                    artist = tag.artist
                    album = tag.album
                    genre = tag.genre
                    year = int(tag.year) if tag.year and tag.year.isdigit() else None # Ensure year is int and numeric
                    duration = tag.duration # in seconds
                    file_size = os.path.getsize(new_full_path)
                    last_modified = os.path.getmtime(new_full_path)

                except Exception as e:
                    print(f"ERROR: Could not read metadata tags from '{new_full_path}'. Skipping this file. Details: {e}")
                    critical_metadata_missing_count += 1
                    continue # Skip to the next file if TinyTag fails

                # Validate critical metadata required for a meaningful entry and fingerprint
                # If any of these are None, we consider it a critical issue.
                if not all([title, artist, album, duration is not None]):
                    print(f"ERROR: Critical metadata (Title, Artist, Album, or Duration) missing for '{new_full_path}'. Skipping this file.")
                    critical_metadata_missing_count += 1
                    continue # Skip to the next file

                # Generate fingerprint ONLY if critical metadata is present
                song_fingerprint = self._generate_song_fingerprint(title, artist, album, duration)
                processed_fingerprints_this_run.add(song_fingerprint)

                # UPSERT logic:
                cursor.execute("""
                    INSERT INTO songs (
                        song_fingerprint, original_path, current_folder_path, current_filename,
                        title, artist, album, genre, year, duration_seconds, file_size_bytes, last_modified_timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(song_fingerprint) DO UPDATE SET
                        original_path = excluded.original_path,
                        current_folder_path = excluded.current_folder_path,
                        current_filename = excluded.current_filename,
                        title = excluded.title,
                        artist = excluded.artist,
                        album = excluded.album,
                        genre = excluded.genre,
                        year = excluded.year,
                        duration_seconds = excluded.duration_seconds,
                        file_size_bytes = excluded.file_size_bytes,
                        last_modified_timestamp = excluded.last_modified_timestamp;
                """, (
                    song_fingerprint, original_path_from_dict, current_folder_path, new_file_name_key,
                    title, artist, album, genre, year, duration, file_size, last_modified
                ))

            # --- Handle deletions
            #     (songs that were in the DB but not in this run) ---
            # Get all fingerprints currently in the database
            cursor.execute("SELECT song_fingerprint FROM songs;")
            all_db_fingerprints = {row[0] for row in cursor.fetchall()}

            # Find fingerprints that are in the DB but NOT in the current run's processed set
            fingerprints_to_delete = all_db_fingerprints - processed_fingerprints_this_run

            if fingerprints_to_delete:
                # Delete these records from the database
                placeholders = ','.join('?' * len(fingerprints_to_delete))
                cursor.execute(f"DELETE FROM songs WHERE song_fingerprint IN ({placeholders})", tuple(fingerprints_to_delete))
                print(f"Deleted {len(fingerprints_to_delete)} records for songs no longer found in the library.")

            conn.commit()
            print(f"Music metadata database '{db_path}' updated successfully.")
            if critical_metadata_missing_count > 0:
                print(f"WARNING: {critical_metadata_missing_count} files were skipped due to missing or unreadable critical metadata. Please check the logs above to identify and fix these files.")

        except sqlite3.Error as e:
            print(f"SQLite error during database update: {e}")
        finally:
            if conn:
                conn.close()

    def print_query(self, results, attribute, search_term):
        """
        Print a list of song dictionaries (from query_music) as a Markdown table.

        Args:
            results (list[dict]): A list of dictionaries, where each dict represents a song.
                                  Expected keys: "title", "artist", "album", "current_path", "original_path".
            attribute (str): The attribute that was queried (e.g., "artist"). Used for header.
            search_term (str): The term that was searched for (e.g., "Beatles"). Used for header.

        Examples:
            >>> m = MusicMan(".")
            >>> my_attr = "artist"
            >>> my_term = "ac/dc"
            >>> r = m.query(my_attr, my_term)
            >>> print_query(r, my_attr, my_term)
        """
        if not results:
            print(f"No results to display for '{search_term}' in '{attribute}'.")
            return

        markdown_output_lines = []
        markdown_output_lines.append(f"### Query Results for '{search_term}' in '{attribute}'")

        # Define column headers and order of display
        # These are the display names, NOT the dictionary keys
        column_display_names = ["Title", "Artist", "Album", "Current Path", "Original Path"]
        # Map display names to the dictionary keys
        column_keys = {
            "Title": "title",
            "Artist": "artist",
            "Album": "album",
            "Current Path": "current_path",
            "Original Path": "original_path"
        }

        # Max widths for internal Markdown padding (initialize with header lengths)
        max_widths = {name: len(name) for name in column_display_names}

        # First pass: Calculate max widths for internal padding based on data
        for row_data in results:
            # Get values, convert None to "N/A" for display length calculation
            title_display = str(row_data.get("title") or "N/A")
            artist_display = str(row_data.get("artist") or "N/A")
            album_display = str(row_data.get("album") or "N/A")
            current_path_display = str(row_data.get("current_path") or "N/A")
            original_path_display = str(row_data.get("original_path") or "N/A")

            max_widths["Title"] = max(max_widths["Title"], len(title_display))
            max_widths["Artist"] = max(max_widths["Artist"], len(artist_display))
            max_widths["Album"] = max(max_widths["Album"], len(album_display))
            max_widths["Current Path"] = max(max_widths["Current Path"], len(current_path_display))
            max_widths["Original Path"] = max(max_widths["Original Path"], len(original_path_display))

        # Generate Header Row for Markdown
        header_parts = []
        separator_parts = []
        for col_name in column_display_names:
            header_parts.append(f"{col_name:<{max_widths[col_name]}}")
            separator_parts.append("-" * max(3, max_widths[col_name])) # Min 3 hyphens for Markdown table

        markdown_output_lines.append("| " + " | ".join(header_parts) + " |")
        markdown_output_lines.append("|-" + "-|-".join(separator_parts) + "-|")

        # Generate Data Rows for Markdown
        for row_data in results:
            data_parts = []
            for col_name in column_display_names:
                # Use the column_keys map to get the correct dictionary value
                key = column_keys[col_name]
                display_value = str(row_data.get(key) or "N/A")
                data_parts.append(f"{display_value:<{max_widths[col_name]}}")
            markdown_output_lines.append("| " + " | ".join(data_parts) + " |")

        # Print the accumulated Markdown table
        print("\n".join(markdown_output_lines))

    def query(self, attribute, search_term):
        """
        Queries the music database for specified attributes.
        Returns a list of dictionaries, where each dictionary represents a song.
        Returns an empty list if no results or database not found.
        """
        db_path = os.path.join(self.base_dir, self.DB_FILE)
        if not os.path.exists(db_path):
            print(f"Database file '{db_path}' not found. Please run MusicMan.run() first.")
            return []

        conn = None
        results_formatted = []
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            valid_attributes = ["title", "artist", "album", "genre", "current_filename", "current_folder_path", "original_path"]
            if attribute not in valid_attributes:
                print(f"Invalid attribute '{attribute}'. Supported attributes: {', '.join(valid_attributes)}")
                return []

            query = f"SELECT title, artist, album, current_folder_path, current_filename, original_path FROM songs WHERE {attribute} LIKE ?"
            cursor.execute(query, (f"%{search_term}%",))
            results_raw = cursor.fetchall()

            if not results_raw:
                # No print here, just return empty list
                return []

            # Process raw tuples into dictionaries
            for row in results_raw:
                title, artist, album, current_folder_path, current_filename, original_path = row
                current_full_path = os.path.join(current_folder_path, current_filename) if current_folder_path and current_filename else None

                results_formatted.append({
                    "title": title,
                    "artist": artist,
                    "album": album,
                    "current_path": current_full_path,
                    "original_path": original_path
                })

        except sqlite3.Error as e:
            print(f"SQLite error during query: {e}")
        finally:
            if conn:
                conn.close()
        return results_formatted

    def assign_new_folders(self):
        """
        Name:     MusicMan.assign_new_folders
        Inputs:   None.
        Outputs:  None.
        Features: Assigns files to a folder path based on the maximum number of
                  files per folder allowed
        """
        j = 1  # folder number
        k = 0  # files per folder number; bookkeeping purposes only
        for my_file in sorted(list(self.file_dict.keys())):
            # Keep track of folders and files:
            k += 1
            if k > self.MAX_SONGS_PER_FOLDER:
                # Reset file per folder counter and increment folder
                k = 1
                j += 1

            if j > (self.MAX_FOLDERS - 1):
                # NOTE: the minus one accounts for root folder
                raise ValueError("Exceeded the allowable number of folders!")

            # Extract previous tuple:
            old_path, _ = self.file_dict[my_file]

            # Assign new output path:
            folder_name = "folder-%02d" % (j)
            folder_path = os.path.join(self.base_dir, folder_name)
            file_path = os.path.join(folder_path, my_file)

            # Update dictionary tuple with new output path:
            self.file_dict[my_file] = (old_path, file_path)

    def clean_up(self):
        """
        Name:     MusicMan.clean_up
        Inputs:   None.
        Outputs:  None.
        Features: Recursively removes empty sub-directories from base directory
        Depends:  find_empty_dirs
        """
        empty_dirs = self.find_empty_dirs()
        while len(empty_dirs) > 0:
            for my_dir in empty_dirs:
                os.rmdir(my_dir)
            empty_dirs = self.find_empty_dirs()

    def find_files(self):
        """
        Name:     MusicMan.find_files
        Inputs:   None.
        Outputs:  None.
        Features: Search base directory for MP3 files using a recursive
                  directory search
        """
        # Reset file list:
        self.file_list = []
        for root, subdirs, files in os.walk(self.base_dir):
            # Filter out hidden directories at the top level of os.walk
            # This is more robust than relying on the caller to filter.
            subdirs[:] = [d for d in subdirs if not d.startswith('.')]

            for my_file in files:
                # Filter out hidden files
                if my_file.startswith('.'):
                    continue

                # Case-insensitive .mp3
                if re.match(r"^.*\.mp3$", my_file, re.IGNORECASE):
                    self.file_list.append(os.path.join(root, my_file))

        if self.num_files > self.MAX_SONGS:
            raise ValueError("Exceeded maximum number of songs allowable!")

    def find_empty_dirs(self):
        """
        Name:     MusicMan.find_empty_dirs
        Inputs:   None.
        Outputs:  list, paths to empty directories
        Features: Searches base directory for empty sub-directories
        """
        # Reset file list:
        empty_dirs = []
        for root, subdirs, files in os.walk(self.base_dir):
            if len(subdirs) == 0 and len(files) == 0:
                empty_dirs.append(root)
        return empty_dirs

    def mkdir_p(self, path):
        """Make directories.

        Includes intermediate directories, as required.

        Notes:
            tzot (2009) "mkdir -p functionality in python," StackOverflow.
            https://stackoverflow.com/a/600612

        Args:
            path (str): Directory path.
        """
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def move_files(self):
        """
        Name:     MusicMan.move_files
        Inputs:   None.
        Outputs:  None.
        Features: Moves files from old to new path
        Depends:  mkdir_p
        """
        for my_file in self.file_dict:
            old_path, new_path = self.file_dict[my_file]
            new_dir = os.path.dirname(new_path)
            if os.path.isdir(new_dir):
                # Move file
                try:
                    shutil.move(old_path, new_path)
                except Exception as e:
                    print(f"Failed to move {old_path} to {new_path}: {e}")
            else:
                # Create directory:
                try:
                    self.mkdir_p(new_dir)
                except:
                    raise
                else:
                    # Move file
                    try:
                        shutil.move(old_path, new_path)
                    except Exception as e:
                        print(f"Failed to move {old_path} to {new_path} after creating dir: {e}")

    def rename_mp3(self, rand_id, file_name):
        """
        Name:     MusicMan.rename_mp3
        Inputs:   - int, random number (rand_id)
                  - str, name of MP3 file (file_name)
        Outputs:  str, new MP3 file name (new_name)
        Features: Renames the new mp3 name, preserving the track title and
                  pre-pending the random ID
        """
        # Allow track numbering "01. Title" and "01 - Title"
        prog = re.compile(
            r"(^\d+([\.-]\d+)?\.?(\s-)?)\s.*\.mp3$",
            re.IGNORECASE  # Case-insensitive
        )
        result = prog.match(file_name)
        if result is not None:
            repl_str = "%04d." % (rand_id)
            new_name = re.sub(
                r"(^\d+([\.-]\d+)?\.?(\s-)?)",
                repl_str,
                file_name,
                count=1,
                flags=re.IGNORECASE
            )
        else:
            print(f"'{file_name}' does not match expected pattern for renaming. Keeping original name.")
            new_name = file_name # Ensure new_name is always assigned

        return new_name

    def run(self):
        """
        Name:     MusicMan.run
        Inputs:   None
        Outputs:  None
        Features: Convenience function for finding, renaming and moving MP3
                  files and cleaning up empty directories
        Depends:  - assign_new_folders (raises exceptions)
                  - clean_up
                  - find_files (raises exceptions)
                  - move_files (raises exceptions)
                  - rename_files
                  - _build_metadata_db
        """
        self.find_files()              # search base directory for MP3 files
        if self.num_files > 0:
            self.set_new_names()       # rename mp3 files
            self.assign_new_folders()  # assign new files to a folder path
            self.move_files()          # move files to new folder
            self.clean_up()            # remove lingering empty directories
            self._build_metadata_db()  # Build the database after everything
        else:
            print("Found no music files! Check your path.")
            # If no files found, delete existing DB to reflect empty library
            db_path = os.path.join(self.base_dir, self.DB_FILE)
            if os.path.exists(db_path):
                try:
                    os.remove(db_path)
                    print(f"No music files found, deleted existing database: {db_path}")
                except OSError as e:
                    print(f"Error deleting database file {db_path}: {e}")

    def set_new_names(self):
        """
        Name:     MusicMan.set_new_names
        Inputs:   None.
        Outputs:  None.
        Features: Initializes file dictionary for new file names and old file
                  paths
        Depends:  rename_mp3
        """
        # Create numbers for randomizing files
        random_ids = [x for x in range(self.num_files)]
        random.shuffle(random_ids)

        # Reset file dictionary:
        self.file_dict = {}
        for i in range(self.num_files):
            fid = random_ids[i]
            file_path = self.file_list[i]
            file_name = os.path.basename(file_path)
            new_file = self.rename_mp3(fid, file_name)
            self.file_dict[new_file] = (file_path, "")


class TagManager(object):
    """A class to analyze and manage MP3 metadata tags.

    This class focuses on identifying and fixing common tag issues like missing
    album names and years, and embedding external album artwork (e.g.,
    album.png) directly into the MP3 files.
    """
    def __init__(self, music_library_root_dir):
        """
        Initializes the MP3TagManager with the root directory of the music library.

        Args:
            music_library_root_dir (str): The root path of your music collection.
        """
        if not os.path.isdir(music_library_root_dir):
            raise ValueError(f"Directory not found: {music_library_root_dir}")
        self.root_dir = music_library_root_dir
        self.mp3_files = [] # To store paths of discovered MP3s
        self.problem_files = {
            'missing_album': [],
            'missing_year': [],
            'no_art_embedded': [],
            'error_processing': []
        }

    def _find_mp3_files(self):
        """
        Internal method to recursively find all MP3 files in the root directory.
        """
        self.mp3_files = []
        print(f"Scanning for MP3 files in: {self.root_dir}...")
        for root, _, files in os.walk(self.root_dir):
            # Skip hidden directories like .git, .Trash, etc.
            if os.path.basename(root).startswith('.'):
                continue
            for file in files:
                if file.lower().endswith('.mp3'):
                    self.mp3_files.append(os.path.join(root, file))
        print(f"Found {len(self.mp3_files)} MP3 files.")

    def analyze_tags(self):
        """
        Analyzes MP3 tags for missing album/year and embedded artwork status.
        Populates self.problem_files with identified issues.
        """
        self._find_mp3_files()

        # Reset problem files from previous analysis
        self.problem_files = {
            'missing_album': [],
            'missing_year': [],
            'no_art_embedded': [],
            'error_processing': []
        }

        print("\nAnalyzing MP3 tags...")
        for i, mp3_path in enumerate(self.mp3_files):
            if (i + 1) % 100 == 0 or (i + 1) == len(self.mp3_files):
                print(f"  Processed {i+1}/{len(self.mp3_files)} files.")

            try:
                audio = MP3(mp3_path, ID3=ID3)
                # Ensure ID3 tags are present, if not, add an empty ID3 tag
                if audio.tags is None:
                    audio.add_tags() # Adds a default ID3 v2.3 tag
                    audio.save() # Save immediately to write the empty tags

                tags = audio.tags

                # Check for Album (TALB)
                if 'TALB' not in tags or not tags['TALB'].text or not tags['TALB'].text[0].strip():
                    self.problem_files['missing_album'].append(mp3_path)

                # Check for Year (TDRC or TYER - TDRC is modern, TYER is old)
                # TDRC is usually "YYYY-MM-DD" or "YYYY", so we'll just check if it exists
                if 'TDRC' not in tags and 'TYER' not in tags:
                    self.problem_files['missing_year'].append(mp3_path)
                elif 'TDRC' in tags and not tags['TDRC'].text:
                     self.problem_files['missing_year'].append(mp3_path)
                elif 'TYER' in tags and not tags['TYER'].text:
                     self.problem_files['missing_year'].append(mp3_path)

                # Check for Album Art (APIC)
                has_artwork = False
                for k, v in tags.items():
                    if k.startswith('APIC'):
                        has_artwork = True
                        break
                if not has_artwork:
                    self.problem_files['no_art_embedded'].append(mp3_path)

            except error as e:
                self.problem_files['error_processing'].append((mp3_path, str(e)))
                print(f"  Error processing {mp3_path}: {e}")
            except Exception as e:
                self.problem_files['error_processing'].append((mp3_path, str(e)))
                print(f"  Unexpected error processing {mp3_path}: {e}")

        self._print_analysis_summary()

    def _print_analysis_summary(self):
        """Prints a summary of the analysis results."""
        print("\n--- Analysis Summary ---")
        print(f"Total MP3 files analyzed: {len(self.mp3_files)}")
        print(f"Files with missing Album tag: {len(self.problem_files['missing_album'])}")
        print(f"Files with missing Year tag: {len(self.problem_files['missing_year'])}")
        print(f"Files with no embedded album art: {len(self.problem_files['no_art_embedded'])}")
        print(f"Files with processing errors: {len(self.problem_files['error_processing'])}")
        print("------------------------")

        if self.problem_files['missing_album']:
            print("\nFiles with Missing Album:")
            for p in self.problem_files['missing_album']:
                print(f"  - {p}")
        if self.problem_files['missing_year']:
            print("\nFiles with Missing Year:")
            for p in self.problem_files['missing_year']:
                print(f"  - {p}")
        if self.problem_files['no_art_embedded']:
            print("\nFiles with No Embedded Album Art:")
            for p in self.problem_files['no_art_embedded']:
                print(f"  - {p}")
        if self.problem_files['error_processing']:
            print("\nFiles with Processing Errors:")
            for p, err in self.problem_files['error_processing']:
                print(f"  - {p} (Error: {err})")

    def embed_album_art(self, dry_run=True, art_filename="Folder.jpg"):
        """
        Embeds album art (e.g., 'Folder.jpg') from the same directory into
        MP3 files.

        Args:
            dry_run (bool):
                If True, only report what would be done, do not modify files.
                If False, actually embed the artwork.
            art_filename (str):
                The name of the artwork file to look for (e.g., "Folder.jpg").
        """
        if not self.mp3_files:
            print("No MP3 files found. Please run analyze_tags() first.")
            return

        print(f"\n--- Embedding Album Art ({'Dry Run' if dry_run else 'Actual Run'}) ---")
        embedded_count = 0
        skipped_no_art_file = 0
        skipped_already_has_art = 0
        error_count = 0

        for i, mp3_path in enumerate(self.mp3_files):
            if (i + 1) % 100 == 0 or (i + 1) == len(self.mp3_files):
                print(f"  Processed {i+1}/{len(self.mp3_files)} files for art embedding.")

            artwork_path = os.path.join(os.path.dirname(mp3_path), art_filename)

            # Check if artwork file exists
            if not os.path.exists(artwork_path):
                # print(f"  No '{art_filename}' found for {mp3_path}. Skipping.")
                skipped_no_art_file += 1
                continue

            try:
                audio = MP3(mp3_path, ID3=ID3)
                # Ensure ID3 tags are present
                if audio.tags is None:
                    audio.add_tags()
                    # No need to save here, will save after adding art

                tags = audio.tags

                # Check if artwork is already embedded (to avoid redundant operations)
                has_artwork = False
                for k, v in tags.items():
                    if k.startswith('APIC'):
                        # Can add a more sophisticated check here if needed (e.g., comparing image data)
                        has_artwork = True
                        break

                if has_artwork:
                    print(f"  {mp3_path} already has embedded artwork. Skipping.")
                    skipped_already_has_art += 1
                    continue

                # Read artwork data
                with open(artwork_path, 'rb') as f:
                    artwork_data = f.read()

                # Remove any existing APIC frames before adding new one, to prevent duplicates
                # This ensures you're replacing, not just adding
                for k in list(tags.keys()): # Use list(tags.keys()) to modify during iteration
                    if k.startswith('APIC'):
                        del tags[k]

                # Create APIC (Attached Picture) frame
                # mime: Mime type (e.g., 'image/png', 'image/jpeg')
                # type: 3 for front cover (other types: 0=other, 1=icon, 2=other icon, etc.)
                # desc: Description (optional)
                # data: The image data
                tags.add(
                    APIC(
                        encoding=3, # 3 is UTF-8
                        mime='image/jpeg',
                        type=3, # 3 is Front Cover
                        desc=u'Cover',
                        data=artwork_data
                    )
                )

                if not dry_run:
                    audio.save()
                    embedded_count += 1
                    print(f"  Embedded '{art_filename}' into {mp3_path}")
                else:
                    print(f"  DRY RUN: Would embed '{art_filename}' into {mp3_path}")

            except error as e:
                error_count += 1
                print(f"  Error processing {mp3_path} for art embedding: {e}")
            except Exception as e:
                error_count += 1
                print(f"  Unexpected error processing {mp3_path} for art embedding: {e}")

        print("\n--- Album Art Embedding Summary ---")
        print(f"Total files considered: {len(self.mp3_files)}")
        print(f"Files where '{art_filename}' was embedded: {embedded_count}")
        print(f"Files where no '{art_filename}' was found: {skipped_no_art_file}")
        print(f"Files already had embedded art (skipped): {skipped_already_has_art}")
        print(f"Files with errors during embedding: {error_count}")
        print("-----------------------------------")


    def fix_missing_tags(self, dry_run=True, default_album="Unknown Album", default_year=None):
        """
        Attempts to fix missing Album and Year tags.
        This method would typically require user input or a more sophisticated
        logic to infer missing data (e.g., from folder names or online databases).
        For now, it reports and can set default values if needed.

        Args:
            dry_run (bool): If True, only report what would be done.
            default_album (str): The default album name to use if missing.
            default_year (int/str): The default year to use if missing.
                                    Set to None to not auto-fill year.
        """
        # This method is more complex as "fixing" missing data often requires
        # human intervention or heuristics.
        # For a basic implementation, we can just report and optionally fill with defaults.

        if not self.problem_files['missing_album'] and not self.problem_files['missing_year']:
            print("No missing album or year tags found to fix.")
            return

        print(f"\n--- Fixing Missing Tags ({'Dry Run' if dry_run else 'Actual Run'}) ---")
        fixed_album_count = 0
        fixed_year_count = 0
        error_count = 0

        # It's better to re-run analysis or pass the actual problem files from analyze_tags
        # For simplicity, let's assume analyze_tags has populated self.problem_files

        files_to_fix = set(self.problem_files['missing_album'] + self.problem_files['missing_year'])

        for i, mp3_path in enumerate(files_to_fix):
            if (i + 1) % 50 == 0 or (i + 1) == len(files_to_fix):
                print(f"  Processed {i+1}/{len(files_to_fix)} files for tag fixing.")

            try:
                audio = MP3(mp3_path, ID3=ID3)
                if audio.tags is None:
                    audio.add_tags() # Add tags if none exist
                    # Do not save here, we'll save after modifications
                tags = audio.tags

                modified = False

                # Fix Album
                if 'TALB' not in tags or not tags['TALB'].text or not tags['TALB'].text[0].strip():
                    if default_album:
                        if not dry_run:
                            tags['TALB'] = TALB(encoding=3, text=[default_album])
                            modified = True
                            fixed_album_count += 1
                        print(f"  {'DRY RUN: ' if dry_run else ''}Set Album to '{default_album}' for: {mp3_path}")
                    else:
                        print(f"  Missing Album for: {mp3_path} (No default set)")

                # Fix Year
                if 'TDRC' not in tags and 'TYER' not in tags:
                    if default_year is not None:
                        if not dry_run:
                            tags['TDRC'] = TDRC(encoding=3, text=[str(default_year)])
                            modified = True
                            fixed_year_count += 1
                        print(f"  {'DRY RUN: ' if dry_run else ''}Set Year to '{default_year}' for: {mp3_path}")
                    else:
                        print(f"  Missing Year for: {mp3_path} (No default set)")
                elif 'TDRC' in tags and not tags['TDRC'].text:
                    if default_year is not None:
                        if not dry_run:
                            tags['TDRC'].text = [str(default_year)]
                            modified = True
                            fixed_year_count += 1
                        print(f"  {'DRY RUN: ' if dry_run else ''}Updated TDRC Year to '{default_year}' for: {mp3_path}")
                elif 'TYER' in tags and not tags['TYER'].text:
                    if default_year is not None:
                        if not dry_run:
                            # It's generally better to use TDRC (ID3v2.4) over TYER (ID3v2.3) if updating
                            del tags['TYER'] # Remove old tag
                            tags['TDRC'] = TDRC(encoding=3, text=[str(default_year)])
                            modified = True
                            fixed_year_count += 1
                        print(f"  {'DRY RUN: ' if dry_run else ''}Updated TYER Year to '{default_year}' for: {mp3_path} (converted to TDRC)")


                if modified and not dry_run:
                    audio.save()
                    # Re-analyze this file if you want to verify fixes immediately after saving
                    # or re-run analyze_tags for the whole set.

            except error as e:
                error_count += 1
                print(f"  Error fixing tags for {mp3_path}: {e}")
            except Exception as e:
                error_count += 1
                print(f"  Unexpected error fixing tags for {mp3_path}: {e}")

        print("\n--- Fixing Missing Tags Summary ---")
        print(f"Album tags {'would be' if dry_run else ''} set: {fixed_album_count}")
        print(f"Year tags {'would be' if dry_run else ''} set: {fixed_year_count}")
        print(f"Files with errors during tag fixing: {error_count}")
        print("----------------------------------")
        if not dry_run and (fixed_album_count > 0 or fixed_year_count > 0):
            print("\nConsider running analyze_tags() again to verify changes.")


##############################################################################
# MAIN
##############################################################################
if __name__ == "__main__":
    # Create an ArgumentParser class object for dealing with command line args
    p = argparse.ArgumentParser(
        description="Randomizes MP3 files within a folder or USB drive.")

    # Add an additional optional argument for music folder path
    # the default (if not given) will be to look locally.
    p.add_argument("-p", "--path", default=".",
                   help="Path to your music folders")

    # Read any command line arguments sent to the program
    # NOTE: if -h or --help, the program stops here
    args = p.parse_args()

    # Create an instance of the music man class and run it
    my_music = MusicMan(args.path)
    my_music.run()
