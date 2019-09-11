#!/usr/bin/env python3
#
# music_randomizer.py
#
# VERSION 0.3.1
#
# LAST EDIT: 2019-09-11
#
# This script randomizes music files on a USB drive
#
##############################################################################
# REQUIRED MODULES
##############################################################################
import errno
import os
import random
import re
import shutil
import sys


##############################################################################
# FUNCTIONS
##############################################################################
def show_help():
    """
    Name:     show_help
    Inputs:   None
    Outputs:  None
    Features: Prints the help text when user uses the '-h' command flag
    """
    help_txt = ("FILE: music_randomizer.py\n"
                "DESC: Randomizes MP3 files within a folder or USB drive.\n"
                "USGE: app_name [options]\n"
                "  -p, --path   path to parent MP3 folder\n"
                "  -h, --help   shows the help text\n")
    print(help_txt)


##############################################################################
# CLASSES
##############################################################################
class MusicMan(object):
    """
    Name:     MusicMan
    Features: Class for randomizing and organizing MP3 files for USB playback
    History:  Version 0.3
              - updated rename mp3 files function [17.01.15]
              Version 0.2
              - use Reader class for mp3 title tag in file remaning [17.01.14]
    """
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Class Parameters
    # ////////////////////////////////////////////////////////////////////////
    MAX_SONGS = 130560           # Denon: 999; Subaru: 130560
    MAX_SONGS_PER_FOLDER = 20
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
        # Intitialize class variables:
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
        """
        Name:     MusicMan.mkdir_p
        Inputs:   str, directory path (path)
        Returns:  None.
        Features: Makes directories, including intermediate directories as
                  required (i.e., directory tree)
        Ref:      tzot (2009) "mkdir -p functionality in python,"
                  StackOverflow, Online:
                  http://stackoverflow.com/questions/600268/
                    mkdir-p-functionality-in-python
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
        prog = re.compile("(^\d+([\.-]\d+)?\.?)\s.*\.mp3$")
        result = prog.match(file_name)
        if result is not None:
            repl_str = "%04d." % (rand_id)
            new_name = re.sub("(^\d+([\.-]\d+)?\.)", repl_str, file_name)
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
        else:
            print("Found no music files!")

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
    # Check command-line arguments
    num_args = len(sys.argv)
    my_dir = None
    if num_args > 3:
        show_help()
        print("Too many arguments given.")
    elif num_args > 1 and num_args < 4:
        if '-p' in sys.argv or '--path' in sys.argv:
            if '-p' == sys.argv[-1] or '--path' == sys.argv[-1]:
                # Bad form!
                show_help()
                print("No path given following '-p' argument.")
            else:
                # Get the path
                my_dir = sys.argv[-1]
                my_music = MusicMan(my_dir)
                my_music.run()
        elif '-h' in sys.argv or '--help' in sys.argv:
            show_help()
        else:
            show_help()
            print('Unrecognized argument.')
    else:
        show_help()
        print('No arguments given.')
