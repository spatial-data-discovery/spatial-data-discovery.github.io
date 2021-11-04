#!/usr/bin/env python3
#
# drive_size.py
#
# This script takes a directory path and determines the folder size
# based on the files found within. The results are also broken down by
# the first-level sub-directories to help determine where the "bulk"
# of drive space is stored.
#
# VERSION 1.0.0
# AUTHOR Tyler W. Davis, CGA
# LAST EDITED 2021-11-04
#
##############################################################################
# IMPORT NECESSARY MODULES
##############################################################################
import argparse
import os


##############################################################################
# IMPORT NECESSARY MODULES
##############################################################################
def format_bytes(size):
    """
    Name:     format_bytes
    Inputs:   int, bytes
    Outputs:  tuple, value w/ units
    Features: Returns a tuple of numerical value and units
    Reference:
    https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb
    """
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'bytes'


def get_top_lv_dirs(d):
    """
    Name:     get_top_lv_dirs
    Inputs:   str,
    Features: Returns a list of subdirectories found in a given directory
    """
    b = []
    for a in os.listdir(d):
        if os.path.isdir(os.path.join(d, a)):
            b.append(a)
    return b


def read_drive(sd):
    """
    Name:     read_drive
    Inputs:   str, search directory path (sd)
    Outputs:  dict, directory names w/ dictionaries of folder/file counts and
              size (in bytes)
    Features: Returns a dictionary of folder sizes, sub-folder counts, and
              file counts
    Depends:  get_top_lv_dirs
    """
    # Initialize the a
    folder_tree = {}

    if os.path.isdir(sd):
        my_dirs = get_top_lv_dirs(sd)
        my_dirs.append(sd)  # add the root dir to end of list

        for cur_dir in my_dirs:
            folder_tree[cur_dir] = {
                'folders': 0,
                'files': 0,
                'size_bytes': 0
            }
            if cur_dir != sd:
                cur_path = os.path.join(sd, cur_dir)
            else:
                cur_path = sd

            for root, dirs, files in os.walk(cur_path):
                for d in dirs:
                    folder_tree[cur_dir]['folders'] += 1
                for f in files:
                    try:
                        fsize = os.stat(os.path.join(root, f)).st_size
                    except:
                        pass
                    else:
                        folder_tree[cur_dir]['files'] += 1
                        folder_tree[cur_dir]['size_bytes'] += fsize
    return folder_tree


##############################################################################
# MAIN
##############################################################################
if __name__ == '__main__':
    # Create an ArgumentParser class object for dealing with commandline args
    p = argparse.ArgumentParser(
        description="Create a report of folder size.")
    p.add_argument("-p", "--path", default=".", help="Path to analyze")
    args = p.parse_args()

    # Print the results:
    my_results = read_drive(args.path)
    my_content = []
    header_txt = "dir,folders,files,size"
    my_content.append(header_txt)
    for k, v in my_results.items():
        ftsize, ftunits = format_bytes(v['size_bytes'])
        my_text = "{},{},{},{:.3f} {}".format(
            k, v['folders'], v['files'], ftsize, ftunits
        )
        my_content.append(my_text)
    for content in my_content:
        print(content)
