#! /usr/bin/env python

# Author: John Hennin
# Last Updated: 2020-11-03
#
# Script Description:
#
# This script simulates a simplified version of roulette.
# There are two different betting options (color bets and straight bets).
# There also three different roulette wheels (No Zero, French, and American).
# The player starts with $1000 and is asked how much they'd like to bet.
# The game possesses utility as a source of entertainment.
# The script requires the numpy module.


# Import Modules
###############################################################################
import os
import sys
import argparse
import warnings

import numpy as np

# Global Variables
###############################################################################
COLORS = ["R", "B"]
B = 0
K = 0


# Functions
###############################################################################
def wipescreen():
    """Clears the terminal window for user"""
    if sys.platform == "darwin" \
            or sys.platform == "linux" \
            or sys.platform == "linux2":
        os.system("clear")
    elif sys.platform == "win32":
        os.system("cls")


def nozero(bet):
    """Simulates a No Zero roulette wheel spin
    There are 36 "pockets" and 36 possible winning pockets
    :param bet: What the user bet; string (R or B)  or integer (1-36)
    :return: What pocket the ball landed in (string or integer)
    """
    if bet in np.arange(1, 37):
        pocket = np.random.randint(37)
    elif bet in COLORS:
        pocket = COLORS[np.random.randint(2)]

    return pocket


def french(bet):
    """Simulates a French/Single Zero roulette wheel spin.
    :param bet: What the user bet; string (R or B)  or integer (1-36)
    :return: What pocket the ball landed in (string or integer)
    """
    if bet in np.arange(1, 37):
        pocket = np.random.randint(38)
        if pocket == 37:
            pocket = 0
    elif bet in COLORS:
        pock = np.random.randint(38)
        if pock in np.arange(1, 37, 2):
            pocket = "R"
        elif pock in np.arange(2, 37, 2):
            pocket = "B"
        else:
            pocket = 0

    return pocket


def american(bet):
    """Simulates an American/Double Zero roulette wheel spin.
    :param bet: What the user bet; string (R or B)  or integer (1-36)
    :return: What pocket the ball landed in (string, float, or integer)
    """
    if bet in np.arange(1, 37):
        pocket = np.random.randint(39)
        if pocket == 37:
            pocket = 0
        elif pocket == 38:
            pocket = 0.0
    elif bet in COLORS:
        pock = np.random.randint(38)
        if pock in np.arange(1, 37, 2):
            pocket = "R"
        elif pock in np.arange(2, 37, 2):
            pocket = "B"
        elif pock == 0:
            pocket = 0
        else:
            pocket = 0.0

    return pocket


def spin(totalmoney):
    """Simulates one spin of roulette wheel.
    :param totalmoney: The money (as a float) the user starts a spin with
    :return: The money (as a float) the user ends a spin with
    """

    # To ignore FutureWarning from 'if bet in np.arange(1, 37)' L51, L65, L87
    warnings.simplefilter(action='ignore', category=FutureWarning)
    wipescreen()
    print("Total: $"+str(totalmoney))
    d = 0
    w = 0
    f = 0
    z = 0
    a = 0
    h = 0

    while a != 1:
        rtype = input("Enter a number to choose the roulette wheel type:\n"
                      "1 for No Zero Roulette\n"
                      "2 for French Roulette (Single Zero)\n"
                      "3 for American Roulette (Double Zero)\n\n")
        try:
            rtype = int(rtype)
            if rtype == 1 or rtype == 2 or rtype == 3:
                a = a + 1
            else:
                wipescreen()
                print("Error: invalid entry. Please try again.")
        except ValueError:
            wipescreen()
            print("Error: invalid entry. Please try again.")

    while d != 1:
        while h != 1:
            betkind = input("Now enter a number to choose a bet type:\n"
                            "1 to place a color bet (red or black)\n"
                            "2 to place a straight bet "
                            "(any integer from 1 to 36)\n\n")
            try:

                betkind = int(betkind)
                if betkind == 1 or betkind == 2:
                    h = h + 1
                else:
                    wipescreen()
                    print("Error: invalid entry. Please try again.")
            except ValueError:
                wipescreen()
                print("Error: invalid entry. Please try again.")
        if betkind == 1:
            while f != 1:
                bet = input("Please enter R for red and B for black.\n\n")
                if bet == "R" or bet == "B":
                    f = f+1
                else:
                    wipescreen()
                    print("Error: invalid entry. Please try again.")
            d = d+1
        elif betkind == 2:
            while z != 1:
                bet = input("Please enter an integer from 1 to 36.\n\n")
                try:
                    bet = int(bet)
                    if bet in np.arange(1, 37):
                        z = z + 1
                    else:
                        wipescreen()
                        print("Error: invalid entry. Please try again.")
                except ValueError:
                    wipescreen()
                    print("Error: invalid entry. Please try again.")
            d = d+1

    while w != 1:
        betamount = input("How much money would you like to bet?\n\n$")
        try:
            betamount = float(betamount)
            if betamount > totalmoney:
                print("You can't bet more than you have! Please"
                      " try an amount less than $"+str(totalmoney)+".")
            elif betamount <= 0:
                wipescreen()
                print("Error: invalid entry. Please try again.")
            else:
                w = w+1
        except ValueError:
            wipescreen()
            print("Error: invalid entry. Please try again.")

    totalmoney = totalmoney-betamount
    print("Total: $"+str(totalmoney))
    if rtype == 1:
        result = nozero(bet)
    elif rtype == 2:
        result = french(bet)
    elif rtype == 3:
        result = american(bet)
    print("You bet on "+str(bet)+" and the result was "+str(result)+".")

    if bet == result:
        if type(bet) == str:
            totalmoney = totalmoney + (betamount*2)
        if type(bet) == int:
            totalmoney = totalmoney + (betamount*36)
        print("Great job! Your new total is: $"+str(totalmoney))

    else:
        print("Better luck next time!")

    return totalmoney


# Main Code
###############################################################################
if __name__ == "__main__":
    description = "This simulates a simplified version of standard roulette." \
                  " You can only place straight bets and color bets." \
                  " Follow the prompts and enjoy!"
    parser = argparse.ArgumentParser(description=description)
    args = parser.parse_args()

    # Main game code
    wipescreen()

    while K != 1:
        initiate = input("Hi! Would you like to play roulette? [y/n] ")
        if initiate == "y":
            totalmoney = spin(1000)
            while B != 1:
                yesorno = input("Would you like to play again? [y/n] ")
                if yesorno == "y":
                    wipescreen()
                    if totalmoney <= 0:
                        print("Sorry, looks like you ran out of money. "
                              "Better luck next time!")
                        sys.exit()
                    else:
                        totalmoney = spin(totalmoney)
                elif yesorno == "n":
                    B = B+1
                    K = K+1
                    print("Okay, have a great day!")
                    sys.exit()
                else:
                    wipescreen()
                    print("Error: invalid entry. Please try again.")
            K = K+1

        elif initiate == "n":
            print("Okay, have a great day!")
            sys.exit()
        else:
            wipescreen()
            print("Error: invalid entry. Please try again.")
