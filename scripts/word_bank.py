def make_word_bank(source, sep = ' '):
    word_list = []
    cur_word = ''
    for letter in source:
        if (letter != sep and letter not in '?!.,:;[]()"' and letter != '\n'):
            cur_word+= letter
        elif ((letter == sep or letter =='\n') and cur_word !=''):
            word_list+= [cur_word]
            cur_word = ''
    if cur_word !='':
        word_list+=[cur_word]
    return word_list
