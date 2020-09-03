# sentiment_analysis.py

# By: Amy Hilla

# Version 1.0

# Last Edit: 2020-09-03

# This script takes .csv files with text data
# and analyzes the text in each row
# it assigns two sentiment scores, assessing subjectivity and polarity
# the sentiment scores are added to the .csv as a new column
# the .csv with sentiment scores is then exported as a new file


####################
# Required Modules  #
####################
import argparse
import pandas as pd
from textblob import TextBlob


####################
#    Function      #
####################
def sentiment_scores():

    # User inputs information about what they want to analyze:
    path_to_file = input('Enter file path to .csv file: ')

    encodingtype = input('Enter encoding type for .csv file: ')

    column_name = input('Enter the name of the column containing text you want to analyze: ')

    new_file_name = input('Enter the name of the new file you want to output: ')

    # read in the file as a pandas dataframe
    alldisc = pd.read_csv(path_to_file, encoding = encodingtype)

    # create an empty list which will store the sentiment scores
    senti = []

    # analyze the text data row by row
    for post in alldisc[column_name]:

        # for each row, first check that the text data is a string
        if type(post) == str:

            # convert to TextBlob object
            blob = TextBlob(post)

            # use TextBlob object attribute .sentiment to calculate sentiment scores
            sent = blob.sentiment

            # add the calculated sentiment scores to the list senti containing all the scores
            senti.append(sent)

        else:
            # if the row being analyzed does not contain string data, add 'invalid' for that row
            # this allows the function to run even if some rows are empty or contain non-string data
            # in the final .csv, the column containing scores will contain 'invalid' for these rows
            senti.append('invalid')

    #add the new list of sentiment scores to the original table
    alldisc['sentiment'] = senti

    #export the table with the sentiment scores to a new .csv
    alldisc.to_csv(new_file_name, encoding = encodingtype)

    # tell the user they have succesfully created a new file with the scores
    return print('Your new .csv with the sentiment scores, ' + str(new_file_name) + ', has been created.')

###################
#      Main       #
###################
if __name__ == "__main__":

    # --help command line description
    parser = argparse.ArgumentParser(description='This script will ask you for a .csv file, with at least one column containing text data that you want to perform sentiment analysis on. Then it will calculate subjectivity and polarity scores and create a new .csv file containing the scores.')
    args = parser.parse_args()

    sentiment_scores()
