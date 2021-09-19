import argparse

def make_word_bank(source, sep = ' '):
    word_list = []
    cur_word = ''
    for letter in source:
        if cur_word in word_list: #if word is already in word bank, skip it
            cur_word = ''
            continue
        elif (letter != sep and letter not in '?!.,:;[]()"' and letter != '\n'): #if the string pulled is not the seperator, punctuations, or a new line, add it
            cur_word += letter
        elif ((letter == sep or letter =='\n') and cur_word !=''): #this line ensures that cur_word is empty when new string is added to it
            word_list+= [cur_word]
            cur_word = ''
        elif cur_word !='':  #this adds the word being built into the word bank
            word_list+=[cur_word]
            cur_word = ''
    if cur_word not in word_list: #this line deals with the very last set of letters the script pulls; if it's not in word bank already, it adds it
        word_list+=[cur_word]
    return word_list

if __name__ == "__main__":
    # Create an ArgumentParser class object for dealing with commandline args
    p = argparse.ArgumentParser(
    description="Creates a word bank of all unique words in inserted sentence.")

    args = p.parse_args()

source = input('what sentence do you want a word bank for? ')
print (make_word_bank(source))
