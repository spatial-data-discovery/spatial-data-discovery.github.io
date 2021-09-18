# text_preprocessing.py

# By: Caroline Wall

# Version 1.0

# Last Edit: 2021-09-18

# This script performs text preprocessing on a .txt file by removing
# stop words, removing numbers, removing punctuation, lowercasing,
# tokenizing, and lemmatizing. It then returns the preprocessed text
# in a .txt file.


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

nltk.download()

# User inputs information about the text
path_to_file = input('Enter file path to .txt file: ')
output_file = input('Enter the name you want for your preprocessed data file: ')
language = input('Enter text language: ')
extra_stops = input('Enter common words in text: ')

# Read in the text
text_file = open('example.txt', 'r')
text = text_file.read()
text_file.close()

# Create list of stopwords, combining NLTK's set with user-inputed words
stop_words = set(stopwords.words(language))
extra_stops = extra_stops.translate(extra_stops.maketrans('','',string.punctuation)).lower()
extra_stops = extra_stops.split(' ')
for item in extra_stops:
    stop_words.add(item)

# Remove all numbers from the text
text_no_nums = text.translate(text.maketrans('','',string.digits))

# Lowercase text and remove all punctuation
clean_text = text_no_nums.translate(text_no_nums.maketrans('','',string.punctuation)).lower()

# Tokenize the text
words = word_tokenize(clean_text)

# Remove stopwords
clean_text_no_stops = [word for word in words if word not in stop_words]

# Perform lemmatization
final_text = []
lemmatizer = WordNetLemmatizer()
for word in clean_text_no_stops:
    lemm_word = lemmatizer.lemmatize(word)
    final_text += [lemm_word]

# Create .txt file of preprocessed data using requested file name
print(final_text, file = open(output_file, 'a'))
print('Your preprocessed text data has been created.')
