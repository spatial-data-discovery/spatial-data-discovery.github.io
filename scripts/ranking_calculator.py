# Xianglu Peng
#
# ranking_calculator.py
#
# Recent Edit: 2020-09-04
#
# This script calculates the ranking of a list of players/students 
# (or anything you want to rank) based on their scores. 
# The file you provide should only include two columns 
# and edit it with exactly the same column names : name, score


##################
# MODULES NEEDED #
##################

import pandas as pd
import argparse
import os
import sys

###############
#  Functions  #
###############


def calculator(datafile,min,num,order):
    #datafile - the path of your data
    #min - the minimum number of rounds in order to be displayed in the ranking
    #num - the number of best scores to be calculated in the average
    #order - acsending or descending order 

    #read the file and get the name of the players
    scores = pd.read_csv(datafile)
    name = list(scores.name.unique())

    #store the scores of each players into dictionary
    score_dic = {}
    for i in range(len(scores)):
        if scores.loc[i]['name'] in score_dic:
            score_dic[scores.loc[i]['name']].append(scores.loc[i]['score'])
        else:
            score_dic[scores.loc[i]['name']] = [scores.loc[i]['score']]


    #find and delete the data of players that have not played at least n number of rounds 
    less_than_any = [key for key in score_dic if len(score_dic[key])< int(min)]
    for key in less_than_any:
        del score_dic[key]

    #sort and calculate the average of the best 5 scores for each players

    if order == "A":
        compare = []
        for i in score_dic:
            score_dic[i].sort()
            total = 0
            for a in range(int(num)):
                total += score_dic[i][a]
            average = total/int(num)
            compare.append((i,average,score_dic[i][0]))
         #give the raking by comparing the average score first and then the best score
        compare.sort(key=lambda element: (element[1], element[2]))
        print("The rankings of these players: ")
        for n in range(len(compare)):
            print(str(n+1) + "  " + compare[n][0] + "    " + str(compare[n][1]))
    if order == "D":
        compare = []
        for i in score_dic:
            score_dic[i].sort(reverse=True)
            total = 0
            for a in range(int(num)):
                total += score_dic[i][a]
            average = total/int(num)
            compare.append((i,average,score_dic[i][0]))
        #give the raking by comparing the average score first and then the best score
        compare.sort(key=lambda element: (element[1], element[2]),reverse=True)
        print("The rankings of these players: ")
        for n in range(len(compare)):
            print(str(n+1) + "  " + compare[n][0] + "    " + str(compare[n][1]))


    
##########
#  Main  #
##########

if __name__ == "__main__":

    parse = argparse.ArgumentParser(description=
            "Prints rankings of numerical data read in through a csv file. Please provide an valid path for your file. \n")
    args = parse.parse_args()

    filename = input("Enter the path to your file:  ")
    min = input("The minimum number of rounds in order to be displayed on the rankings:  ")
    num = input("The number of best scores you want to be calculated in the average (CANNOT be greater than the min number you have entered):  ")
    order = input("The order of you want calculate the rankings(Enter A or D):  ")
    calculator(filename,min,num,order)