# file_remover.py

# By: Katherine Lannen

# Version 1.0

# Last Edit: 2020-11-20

# Purpose: This script takes in the path to a directory from which you want to
# delete all files of a certain type and what that type/extension is (e.g. .py
# or .ini) and removes all files of that type within that directory 
# recursively.

##############################################################################
# Required Modules  
##############################################################################
import argparse
import os

##############################################################################
#    Function      
##############################################################################
def file_remover():
    """
    Name:       file_remover()
    Inputs:     No parameters, there are 2 user inputs during runtime
                - str representing the path to a desired directory
                - str representing the desired extension to be removed
    Outputs:    Prints the removed files' paths
    Features:   Delete files with the specified extension recursively within
                the given directory
    """

    path = input('Enter the path to a directory you want to delete from: ')
    file_type = input('Enter the extension you want to remove (.py, .ini): ')

    if os.path.exists(path):
        if os.path.isdir(path):
            for root, folders, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    extension = os.path.splitext(file_path)[1]
                    if extension == file_type:
                        if not os.remove(file_path):
                            print("Deleted: " + str(file_path))
        else:
            print("Path is not a directory")
    else:
        print("Path is not valid")

##############################################################################
#      Main       
##############################################################################
if __name__ == "__main__":
    description = """This script takes in the path to a directory from which\n
    you want to delete all files of a certain type and what that \n
    type/extension is (e.g. .py or .ini) and recursively removes all files \n
    of that type within that directory."""
    
    parser = argparse.ArgumentParser(description=description)
    args = parser.parse_args()

    file_remover()