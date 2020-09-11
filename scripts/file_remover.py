# file_remover.py

# By: Katherine Lannen

# Version 1.0

# Last Edit: 2020-09-03

# This script takes in the path to a directory from which you want to delete all
# files of a certain type and what that type/extension is (e.g. .py or .ini) and 
# removes all files of that type within that directory.

####################
# Required Modules  #
####################
import argparse
import os

####################
#    Function      #
####################
def file_remover():
    path = input('Enter the path to a directory you want to delete a file type from: ')
    file_type = input('Enter the extension you want to remove (ex: .py or .ini): ')

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

##################
#      Main       #
###################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This script takes in the path to a directory from which you want to delete all files of a certain type and what that type/extension is (e.g. .py or .ini) and removes all files of that type within that directory.')
    args = parser.parse_args()
    file_remover()