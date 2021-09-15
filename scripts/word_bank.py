def make_word_bank(source, sep = ' '):
    word_list = []
    cur_word = ''
    for letter in source:
        if cur_word in word_list:
            cur_word = ''
            continue
        elif (letter != sep and letter not in '?!.,:;[]()"' and letter != '\n'):
            cur_word += letter
        elif ((letter == sep or letter =='\n') and cur_word !=''):
            word_list+= [cur_word]
            cur_word = ''
        elif cur_word !='':
            word_list+=[cur_word]
            cur_word = ''
    return word_list

source = input('what sentence do you want a word bank for?')
make_word_bank(source)
