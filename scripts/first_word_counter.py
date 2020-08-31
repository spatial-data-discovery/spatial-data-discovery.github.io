# first_word_counter.py

# By: Ryan Han

# VERSION 1.0

# Last Edit: 2020-02-10

# This script takes .txt or .md files and a word of your choice and returns
# each sentence/sentences where the specified word is the first word. The code
# also prints out the number of times the 'word' appears as the first word.

####################
# Required Module  #
####################
import argparse

####################
#    Function      #
####################

def first_word_counter():
    # Asking user for file name and word
    file_name = input("Enter file name: ")
    word = input("Enter a word you would like to count in the file: ")

    # Allows me to press enter to access default sample .txt file
    if len(file_name) < 1 : file_name = "mbox-short.txt"

    # Opening specified file
    open_file = open(file_name) # Opening said file name

    # Establishing "count" at 0
    count = 0
    # Starting loop to examine every line in file
    for line in open_file:
        # striping the lines of white space
        line = line.rstrip()
        # Once line with word is found
        if line.startswith(word):
            # each line split into each characters, the characters make up the variable words.
            words = line.split()
            # print whole sentence
            print(line)
            # at the end of loop add 1 to count
            count = count + 1

    # Proper grammar
    if count == 1:
        print("There is " + str(count) + " line in the file with " + "'" + word + "'" + " as the first word.")
    else:
        print("There are " + str(count) + " lines in the file with " + "'" + word + "'" + " as the first word.")

###################
#      Main       #
###################
if __name__ == '__main__':
    # --help command line description
    parser = argparse.ArgumentParser(
    description = "This script will ask you for a .txt/.md file and word of your choice. Then it will figure out how many times your word starts a sentence in the file.")
    args = parser.parse_args()

    first_word_counter()
