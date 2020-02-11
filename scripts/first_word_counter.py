import argparse

def first_word_counter():
    file_name = input("Enter file name: ") # Asking for the file name
    word = input("Enter a word you would like to count in the file: ")
    if len(file_name) < 1 : file_name = "mbox-short.txt"
    open_file = open(file_name) # Opening said file name
    count = 0 # Establishing "count" at 0
    for line in open_file: # starting a "for" loop that will examine every line in the file
        line = line.rstrip() # striping the lines of white space
        #if not line.startswith("From:"): continue   #if the lines start with "From:" then you can skip them and go back to top of the loop
        if line.startswith(word): # if the line starts with "From" then you can move on to the rest of the program.
            words = line.split() # each line is split into each character, then those characters make up the variable words.
            print(line) # all of the lines that start with From will have the character in subsection 1 printed.
            count = count + 1 # each time the loop hits here, a 1 is added to the total count
    if count == 1:
        print("There is " + str(count) + " line in the file with " + word + " as the first word.")
    else:
        print("There are " + str(count) + " lines in the file with " + "'" + word + "'" + " as the first word.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description = "Input a .txt file and word of your choice. This script will figure out how many times your word starts a sentence in the file.")
    args = parser.parse_args()
    first_word_counter()
