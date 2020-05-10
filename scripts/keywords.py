import collections
import pandas as pd0
import argparse
import sys
if __name__ == "__main__":
    # Check command-line arguments



    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='The point of this script is to help summarize long readings.It finds the most used words in a text and returns shorter and simpler articles which go over these concepts.')
    args=parser.parse_args()

    try:
        file = open("NDFM.txt")
    except FileNotFoundError:
        print('File does not exist')
        sys.exit()
    #file = open('NDFM.txt', encoding="utf8")#input file
    a= file.read()


    # Stopwords in text file
    try:
        stopwords = set(line.strip() for line in open('stopwords.txt'))
        stopwords = stopwords.union(set(['mr','mrs','one','two','said']))
    except FileNotFoundError:
        print('File does not exist')
        sys.exit()


    wordcount = {}
    for word in a.lower().split():
        word = word.replace(".","")
        word = word.replace(",","")
        word = word.replace(":","")
        word = word.replace("\"","")
        word = word.replace("!","")
        word = word.replace("?","")
        if word not in stopwords:
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1
    # Print most common word
    n_print = int(input("How many key words to google?: "))

    word_counter = collections.Counter(wordcount)
    googleString=""
    for word, count in word_counter.most_common(n_print):
        googleString = googleString +" "+ word

    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")
    for j in search(googleString, tld="co.in", num=10, stop=5, pause=2):
        print(j)

    file.close()
