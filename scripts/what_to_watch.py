#what_to_watch.py
#
# Author: Natalie Larsen
#
# Last Edit: 2020-09-04
#
#This script takes movie or show titles input by the user
#and outputs one for the user to watch next.
#Example user input:
#The Princess Bride,,1917,,Monsters, Inc.,,Once Upon a Time... In Hollywood
# If the result isn’t satisfying,
#the user has the option to re-pick.
#
#Required Modules
import random
import argparse
import sys

#Randomly pick a title from a list, and return choice
def pick_title():
    to_watch = random.choice(user_list)
    print("You should watch:", to_watch)

#Give user the option to re-pick
def new_title():
    pick_again = input("Do you want us to pick again? (y/n): ")
    #If user wants to re-pick, run pick_title function
    if pick_again == "y":
        pick_title()
        new_title()
    elif pick_again == "n":
        print("Happy viewing!")
    #Handle user inputs other than y or n
    else:
        print("Sorry we didn't get that, please answer y or n.")
        new_title()


if __name__ == "__main__":
    #Support for --help or -h command-line arguments
    p = argparse.ArgumentParser(
    description = "This script takes a list of movies/shows input by the user \
    (ex. movie1,,movie2,,movie3,,etc.) and returns one to watch.")
    args = p.parse_args()

    #Get user input,
    #taking into account punctuation in titles
    print("Can't decide what to watch? Let us help!")
    user_input = input("Enter a list of movies/shows, separating titles with two commas(A,,B):\n")

    #Turn input into list
    if ',,' in user_input:
        user_list = user_input.split(',,')
        print("You input the following choices:", user_list)
    #Handle unacceptable user inputs
    else:
        print("Please enter more than one title, separated by two commas(,,).")
        sys.exit()

    pick_title()
    new_title()
