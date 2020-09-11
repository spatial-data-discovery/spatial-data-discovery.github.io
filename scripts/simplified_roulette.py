import numpy as np
import os
import sys
import argparse

#Options for color bets
colors=["R","B"]

#Help message
if __name__ == "__main__":
    parser= argparse.ArgumentParser(description="This is a simplified version of standard roulette. You can only place straight bets and color bets. Follow the prompts and enjoy!")
    args = parser.parse_args()

#Clears screen (purely aesthetics)
def wipescreen():
    if sys.platform=="darwin" or sys.platform=="linux" or sys.platform=="linux2":
        os.system("clear")
    elif sys.platform=="win32":
        os.system("cls")

#No Zero roulette wheel spin (best odds: 36 pockets, 36 possible winning pockets)
def NoZero(bet):
    if bet in np.arange(1,37):
        pocket=np.random.randint(37)
    elif bet in colors:
        pocket=colors[np.random.randint(2)]
    return pocket

#French roulette wheel spin (second best/second worst odds: 37 pockets, 36 possible winning pockets)
def French(bet):
    if bet in np.arange(1,37):
        pocket=np.random.randint(38)
        if pocket==37:
            pocket=0
    elif bet in colors:
        pock=np.random.randint(38)
        if pock in np.arange(1,37,2):
            pocket="R"
        elif pock in np.arange(2,37,2):
            pocket="B"
        else:
            pocket=0
    return pocket

#American roulette wheel spin (worst odds, 38 pockets, 36 possible winning pockets)
def American(bet):
    if bet in np.arange(1,37):
        pocket=np.random.randint(39)
        if pocket==37:
            pocket=0
        elif pocket==38:
            pocket=0.0
    elif bet in colors:
        pock=np.random.randint(38)
        if pock in np.arange(1,37,2):
            pocket="R"
        elif pock in np.arange(2,37,2):
            pocket="B"
        elif pock==0:
            pocket=0
        else:
            pocket=0.0
    return pocket

#One complete round
def spin(total):
    wipescreen()
    print("Total: $"+str(total))
    d=0
    w=0
    f=0
    z=0
    rtype=int(input("Enter 1 for No Zero Roulette, 2 for French Roulette (Single Zero), and 3 for American Roulette (Double Zero). "))
    while d!=1:
        betkind=int(input("Now enter 1 to place a color bet (red or black) and 2 to place a straight bet (any integer from 1 to 36). "))
        if betkind==1:
            while f!=1:
                bet=input("Please enter R for red and B for black. ")
                if bet=="R" or bet=="B":
                    f=f+1
                else:
                    print("Error: unknown input. Please try again.")
            d=d+1
        elif betkind==2:
            while z!=1:
                bet=int(input("Please enter an integer from 1 to 36. "))
                if bet in np.arange(1,37):
                    z=z+1
                else:
                    print("Error: unknown input. Please try again.")
            d=d+1
        else:
            print("Error: unknown input. Please try again.")
    while w!=1:
        betamount=float(input("How much money would you like to bet? $"))
        if betamount>total:
            print("You can't bet more than you have! Please try an amount less than "+str(total))
        elif betamount<=0:
            print("Error: invalid entry. Please try again.")
        else:
            w=w+1
    total=total-betamount
    print("Total: $"+str(total))

    if rtype==1:
        result=NoZero(bet)

    elif rtype==2:
        result=French(bet)

    elif rtype==3:
        result=American(bet)

    print("You bet on "+str(bet)+" and the result was "+str(result))

    if bet==result:
        if type(bet)==str:
            total=total+(betamount*2)
        if type(bet)==int:
            total=total+(betamount*36)
        print("Great job! Your new total is: $"+str(total))
    else:
        print("Better luck next time!")

    return total

#As soon as "python simplified_roulette.py" is entered, clear the screen for game
wipescreen()

#Main game code
initiate=input("Hi! Would you like to play roulette? [y/n] ")
if initiate=="y":
    total=spin(1000)
    b=0
    while b!=1:
        yesorno=input("Would you like to play again? [y/n] ")
        if yesorno=="y":
            wipescreen()
            if total<=0:
                print("Sorry, looks like you ran out of money. Better luck next time!")
                sys.exit()
            else:
                total=spin(total)
        elif yesorno=="n":
            b=b+1
            print("Okay, have a great day!")
            sys.exit()
elif initiate=="n":
    print("Okay, have a great day!")
    sys.exit()

