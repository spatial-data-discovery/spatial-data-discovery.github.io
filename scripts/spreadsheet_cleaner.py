#!/usr/bin/env python3
#
# VERSION 0.1
#
# LAST EDIT: 2019-09-17
#
# This script removes leading, trailing, and duplicate spaces in
# .xls and .xlsx files and creates a new .xlsx file
#
##############################################################################
# REQUIRED MODULES
##############################################################################
import pandas as pd
import os
import re
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
    help_txt = ("FILE: \t spreadsheet_cleaner.py\n"
                "DESC: \t Removes leading, trailing, and duplicate spaces\n"
                "\t in .xlsx and .xls files in a given directory.\n"
                "\t User will be prompted for path to directory\n"
                "\t containing Excel files.\n"
                "NOTE: \t Do not run on files that are currently open.\n"
                "USGE: \t app_name [options]\n"
                "\t -h, --help   shows the help text\n")
    print(help_txt)


##############################################################################
# CLASSES
##############################################################################
class SpreadSheet(object):
    """
    Name:     SpreadSheet
    Features: Class for cleaning Excel files
    History:  Version 0.1
              - Written for class
              - Intended to help with Honors data cleaning
    """
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Class Parameters
    # ////////////////////////////////////////////////////////////////////////
    # None

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Class Initialization
    # ////////////////////////////////////////////////////////////////////////
    def __init__(self, base_dir):
        """
        Name:       SpreadSheet.__init__
        Inputs:     str, base directory (base_dir)
        Features:   Initializes the SpreadSheet class
        Reference:  Way of checking directory is from Prof. Davis's music_randomizer
        """
        # Intitialize class variables:
        self.file_list = []
        if os.path.isdir(base_dir):
            self.base_dir = base_dir
        else:
            self.base_dir = None
            raise OSError("Directory '%s' does not exist" % (base_dir))

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Class Property Definitions
    # ////////////////////////////////////////////////////////////////////////
    # None

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Class Function Definitions
    # ////////////////////////////////////////////////////////////////////////
    def cleaning(self, file, name):
        """
        Name:       SpreadSheet.cleaning
        Inputs:     Excel file
        Outputs:    New, clean .xlsx file
        Features:   Removes whitespace and duplicate spaces from pd dataframes and saves new file.
        Reference:  https://stackoverflow.com/questions/1546226/simple-way-to-remove-multiple-spaces-in-a-string/1546244
        """
        data = pd.read_excel(file, index_col=None, header=0)
        col_names = list(data.columns)
        for col in col_names:
            data[col] = data[col].astype(str)
            data[col] = data[col].str.strip()
            data[col] = data[col].str.replace('[ \t\n\r]+', " ")
        writer = pd.ExcelWriter(name, engine='xlsxwriter')
        data.to_excel(writer, index=False)
        writer.save()

    def get_files(self, base_dir):
        """
        Name:     SpreadSheet.get_files
        Inputs:   None.
        Outputs:  None.
        Features: Creates a list of .xls and .xlsx files in the base directory
        Reference: https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
        """
        directory = base_dir
        # have already checked if directory exists.
        for filename in os.listdir(directory):
            if filename.endswith(".xls") or filename.endswith(".xlsx"):
                self.file_list.append(os.path.join(directory, filename))
            else:
                continue

    def run(self, base_dir):
        """
        Name:       SpreadSheet.run
        Inputs:     file (from get_files), col_names (from get_columns)
        Outputs:    Clean files
        Features:   Cleans Excel files and returns renamed files
        Reference:
        """
        self.get_files(base_dir)
        for file_name in self.file_list:
            names = str(file_name).split(".")
            new_name = "." + str(names[1]) + "_tidy." + str(names[2])
            self.cleaning(file_name, new_name)

##############################################################################
# MAIN
##############################################################################
if __name__ == "__main__":
    if '-h' in sys.argv or '--help' in sys.argv:
        show_help()
    else:
        input_path = str(input("Type path to directory: "))
        utility = SpreadSheet(input_path)
        utility.run(input_path)
