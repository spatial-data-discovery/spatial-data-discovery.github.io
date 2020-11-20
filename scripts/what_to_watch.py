#!/usr/bin/env python3
#
# what_to_watch.py
#
# AUTHOR: Natalie Larsen
#
# LAST EDIT: 2020-11-20
#
# Purpose:
# This script takes movie or show titles input by the user
# and output one for the user to watch next.
# If the result isn’t satisfying,
# the user has the option to re-pick.
#
##############################################################################
# REQUIRED MODULES
##############################################################################
import argparse
import sys
import random


##############################################################################
# FUNCTIONS
##############################################################################
def pick_title():
    """Randomly choose title from user input,
    and return chosen title to user.
    """
    to_watch = random.choice(user_list) #Choose title from user list
    print("You should watch:", to_watch)

def new_title():
    """Give the user the option to re-pick."""
    pick_again = input("Do you want us to pick again? (y/n): ")
    if pick_again == "y":
        pick_title()
        new_title()
    elif pick_again == "n":
        print("Happy viewing!")
        sys.exit()
    else:
        print("Sorry we didn't get that, please answer y or n.")
        new_title()


##############################################################################
# MAIN
##############################################################################
if __name__ == "__main__":
    script_desc = "This script takes a list of movies/shows input by the user \
                  (ex. movie1,,movie2,,movie3,,etc.) and returns one to watch."
    p = argparse.ArgumentParser(description = script_desc)
    args = p.parse_args()

    print("\nCan't decide what to watch? Let us help!\n")
    print("Enter a list of movies/shows!")
    user_input = input("Separate titles with two commas(A,,B,,etc.):\n")
    if ',,' in user_input:
        user_list = user_input.split(',,') #Turn input into list
        print("You input the following choices:", user_list)
    else:
        print("Please enter more than one title, separated by two commas(,,).")
        sys.exit()

    pick_title()

    new_title()
