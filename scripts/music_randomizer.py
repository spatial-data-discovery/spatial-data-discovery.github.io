#!/usr/bin/env python3
#
# music_randomizer.py
#
# VERSION 0.3.4
#
# LAST EDIT: 2025-02-23
#
# This script randomizes music files on a USB drive
# TODO: add mutagen for searching and tag writing.
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


##############################################################################
# CLASSES
##############################################################################
class MusicMan(object):
    """
    Class for randomizing and organizing MP3 files for USB playback.

    Notes:
        Change requests:
            -   Add method to read mp3 track title and artist from file.
                Track titles are in in file names.
                After 'find_files' and 'set_new_names', the file_dict value
                tuples have the old and new paths.
                See also 'audio-metadata' and 'tinytag' Python packages.
            -   Add method to display track titles, artists, and file name.
            -   Add method to search for a track title or artist.
            -   Skip hidden folders (currently finds files in .Trash on USB)

        History:
            Version 0.4:
                -   create SQLite3 database for querying songs
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
        """Generate a consistent hash for a song based on its core metadata."""
        # Normalize and concatenate key metadata fields
        # Use lowercase and strip whitespace for robustness
        data = f"{artist or ''}|{album or ''}|{title or ''}|{duration_seconds or 0.0}"
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

            # Iterate through the file_dict, which now has the final paths
            for new_file_name, (original_path, new_full_path) in self.file_dict.items():
                if not os.path.exists(new_full_path):
                    print(f"Warning: File not found at {new_full_path}. Skipping metadata extraction.")
                    continue

                current_folder_path = os.path.dirname(new_full_path)

                # Initialize with defaults in case of metadata read errors
                title, artist, album, genre, year = "Unknown Title", "Unknown Artist", "Unknown Album", None, None
                duration, file_size, last_modified = 0.0, 0, 0.0

                try:
                    tag = TinyTag.get(new_full_path)
                    title = tag.title or title
                    artist = tag.artist or artist
                    album = tag.album or album
                    genre = tag.genre
                    year = int(tag.year) if tag.year else None
                    duration = tag.duration # in seconds
                    file_size = os.path.getsize(new_full_path)
                    last_modified = os.path.getmtime(new_full_path)

                except Exception as e:
                    print(f"Warning: Could not read metadata for {new_full_path}: {e}. Using defaults.")

                song_fingerprint = self._generate_song_fingerprint(title, artist, album, duration)
                processed_fingerprints_this_run.add(song_fingerprint)

                # UPSERT logic:
                # 1. Try to INSERT.
                # 2. ON CONFLICT (song_fingerprint), DO UPDATE the path and other relevant fields.
                #    We update all fields, as a shuffle means new paths, and user might have
                #    edited tags manually between runs.
                cursor.execute("""
                    INSERT INTO songs (
                        song_fingerprint, original_path, current_folder_path, current_filename,
                        title, artist, album, genre, year, duration_seconds, file_size_bytes, last_modified_timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(song_fingerprint) DO UPDATE SET
                        original_path = excluded.original_path,
                        current_folder_path = excluded.current_folder_path,
                        current_filename = excluded.current_filename,
                        title = excluded.title, -- Update title, artist etc. too, in case tags were changed
                        artist = excluded.artist,
                        album = excluded.album,
                        genre = excluded.genre,
                        year = excluded.year,
                        duration_seconds = excluded.duration_seconds,
                        file_size_bytes = excluded.file_size_bytes,
                        last_modified_timestamp = excluded.last_modified_timestamp;
                """, (
                    song_fingerprint, original_path, current_folder_path, new_file_name,
                    title, artist, album, genre, year, duration, file_size, last_modified
                ))

            # --- Handle deletions (songs that were in the DB but not in this run) ---
            # Get all fingerprints currently in the database
            cursor.execute("SELECT song_fingerprint FROM songs;")
            all_db_fingerprints = {row[0] for row in cursor.fetchall()}

            # Find fingerprints that are in the DB but NOT in the current run's processed set
            fingerprints_to_delete = all_db_fingerprints - processed_fingerprints_this_run

            if fingerprints_to_delete:
                # Delete these records from the database
                placeholders = ','.join('?' * len(fingerprints_to_delete))
                cursor.execute(f"DELETE FROM songs WHERE song_fingerprint IN ({placeholders})", tuple(fingerprints_to_delete))
                print(f"Deleted {len(fingerprints_to_delete)} records for missing songs from database.")

            conn.commit()
            print(f"Music metadata database '{db_path}' updated successfully.")

        except sqlite3.Error as e:
            print(f"SQLite error during database update: {e}")
        finally:
            if conn:
                conn.close()

    def query_music(self, attribute, search_term):
        """
        Queries the music database for specified attributes.
        Returns results including title, artist, album, and current file path.
        """
        db_path = os.path.join(self.base_dir, "music_metadata.db")
        conn = None
        results = []
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Valid attributes to prevent SQL injection for attribute name
            valid_attributes = ["title", "artist", "album", "genre", "current_filename", "current_folder_path"]
            if attribute not in valid_attributes:
                print(f"Invalid attribute '{attribute}'. Supported attributes: {', '.join(valid_attributes)}")
                return results

            # Use LIKE for partial matching, and parameter binding for search_term
            # Select relevant display fields
            query = f"SELECT title, artist, album, current_folder_path, current_filename FROM songs WHERE {attribute} LIKE ?"
            cursor.execute(query, (f"%{search_term}%",))
            results = cursor.fetchall() # Returns a list of tuples

        except sqlite3.Error as e:
            print(f"SQLite error during query: {e}")
        finally:
            if conn:
                conn.close()
        return results


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
        Features: Searches base directory for MP3 files using a recursive
                  directory search

        @TODO:
        * skip hidden files or folders
          http://stackoverflow.com/questions/13454164/
            os-walk-without-hidden-folders
        """
        # Reset file list:
        self.file_list = []
        for root, subdirs, files in os.walk(self.base_dir):
            for my_file in files:
                if re.match("^.*mp3$", my_file):
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
                shutil.move(old_path, new_path)
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
                    except:
                        print("%s ... failed" % (old_path))

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
        prog = re.compile("(^\d+([\.-]\d+)?\.?(\s-)?)\s.*\.mp3$")
        result = prog.match(file_name)
        if result is not None:
            repl_str = "%04d." % (rand_id)
            new_name = re.sub("(^\d+([\.-]\d+)?\.?(\s-)?)", repl_str, file_name)
        else:
            print("%s ... FAILED" % (file_name))
            new_name = file_name

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
        """
        self.find_files()              # search base directory for MP3 files
        if self.num_files > 0:
            self.set_new_names()       # rename mp3 files
            self.assign_new_folders()  # assign new files to a folder path
            self.move_files()          # move files to new folder
            self.clean_up()            # remove lingering empty directories
            self._build_metadata_db()  #
        else:
            print("Found no music files! Check your path.")

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
