#!/usr/bin/env python3
#
# create_corpus.py
#
# VERSION 0.3.2
#
# Last edit: 2021-09-18
#
# This preliminary script will take a given input text...
# (single column dataframe or single string)
# ...stem the unique non-stopwords, and create a corpus
#
##############################################################################
# REQUIRED MODULES
##############################################################################

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk
import heapq
import re
import pandas as pd


nltk.download('stopwords')
nltk.download('punkt')

pt = PorterStemmer()

##############################################################################
# FUNCTIONS
##############################################################################

def df_corpus(df):
        """
        Name:     df_corpus
        Inputs:   pandas DataFrame (df)
        Outputs:  pandas DataFrame (corpus)
        Features: Isolates, lowercases, and stems all unique, non_stopwords.

        """
    unique_df = []
    for i in range(len(df)):
        ent = re.sub('[^a-zA-Z0-9 ]','', df[i])
        ent = des.lower()
        ent = des.split()
        ent = [word for word in ent if not word in set(stopwords.words('english'))]
        ent = [pt.stem(word) for word in ent]
        ent = ' '.join(ent)
        unique_df.append(ent)

    corpus_df = []
    for i in range(len(df)):
        corpus_df = set(corpus_df).union(set(unique_df[i].split(' ')))

    return pd.DataFrame(list(corpus_df), columns=['Unique Words'])


def txt_corpus(path):
            """
            Name:     txt_corpus
            Inputs:   str, directory path (path)
            Outputs:  pandas DataFrame (corpus)
            Features: Isolates, lowercases, and stems all unique, non_stopwords.

            """
    file = open(path, encoding='utf-8').read()
    sent = nltk.word_tokenize(file)
    for i in range(len(sent)):
        sent[i] = sent[i].lower()
        sent[i] = re.sub(r'\W', ' ', sent[i])
        sent[i] = re.sub(r'\s+', ' ', sent[i])

    unique_txt = []
    for i in range(len(sent)):
        txt = re.sub('[^a-zA-Z0-9 ]','', sent[i])
        txt = txt.lower()
        txt = txt.split()
        txt = [word for word in txt if not word in set(stopwords.words('english'))]
        txt = [pt.stem(word) for word in txt]
        txt = ' '.join(txt)
        unique_txt.append(txt)

    for i in range(unique_txt.count('')):
        unique_txt.remove('')

    corpus_txt = []
    for i in range(len(unique_txt)):
        corpus_txt = set(corpus_txt).union(set(unique_txt[i].split(' ')))

    return pd.DataFrame(list(corpus_txt), columns=['Unique Words'])

##############################################################################
# MAIN
##############################################################################

x = input('Are you passing a .txt file? (Y or N): ')

if x=='Y':
    y = input('Paste the path to your .txt file: ')
    var_Y = txt_corpus(y)
    print(var_Y)

else:
    z = input('Paste the stored variable for your single column dataframe: ')
    var_N = df_corpus(z)
    print(var_N)
