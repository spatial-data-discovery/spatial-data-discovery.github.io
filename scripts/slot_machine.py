#slot_machine.py
#
#Author: Abby Gaddi
#
#Date: 2020-02-10
#
#This script was used in a lab from my Machine Learning classs last semester.
#It shows how Upper Confidence Boundary reinforcment learning is used with machine slots as an example,
#and prompts the user for the starting balance and trial number.
#
#
#LIBRARIES
import random
import math
import argparse


#Slot machine odds function given from class
def playSlots(machine):

    if(machine == 1):
        return round(random.uniform(0,1),2)

    if(machine == 2):
        return round(random.uniform(0.5,1.5),2)

    if(machine>=3 and machine <=10):
        return round(random.triangular(0,0.5,1),2)

    if(machine >=11 and machine <=14):
        return round(random.triangular(0.5,1,1.5),2)

    if(machine == 15):
        return round(random.triangular(0.8,1,3.0),2)

    if(machine >= 16 and machine <= 20):
        return round(random.uniform(0,1.1),2)

    if(machine >20):
        print("There are only 20 slot machines!  You've gone awry.")


def calculate_UCB(balance,N):

    #VARIABLES
    #number of slot machines
    d = 20
    #used for the machine/computer to learn
    machine_record = []
    award_record = []
    number_of_selections = [0] * d
    sum_of_rewards = [0] * d

    #UPPER CONFIDENCE BOUND REINFORCEMENT LEARNING
    for n in range(0,N):

        #initialize the machine choice at one
        machine_choice = 1
        #define the max upper bound, based on the mean and maximum return value
        max_upper_bound = 0

        #calculating which machine has the best return value so it is constantly picked
        for i in range(1,d):
            if number_of_selections[i] > 0:
                #calculate the average money got back
                average_award = sum_of_rewards[i] / number_of_selections[i]
                #calculate the money the machine thinks it will get back
                delta_i = math.sqrt(3/2*math.log(n+1)/number_of_selections[i])
                upper_bound = average_award + delta_i
            else:
                #if the machine is being used for the first time, set the upperbound very high to force the computer to test it
                upper_bound = 1e200

            if upper_bound > max_upper_bound:
                max_upper_bound = upper_bound
                #choose the machine with the highest upper bound
                machine_choice = i

        #calculate earnings/balance
        machine_record.append(machine_choice)
        number_of_selections[machine_choice] = number_of_selections[machine_choice] + 1
        award = playSlots(machine=machine_choice)
        sum_of_rewards[machine_choice] = sum_of_rewards[machine_choice] + award
        award_record.append(award)
        balance = balance - 1 + award
        return('You won: $' + str(round(balance,2))+'\n Machine ' + str(sum_of_rewards.index(max(sum_of_rewards))) +' won you the most money' )
        

#MAIN
if __name__ == '__main__':
    p = argparse.ArgumentParser(description =  "Play an unrealistic slot machine simulator by gambling an amount you want to play with\
         and see which machine has the best cash reward.")
    args = p.parse_args()

    balance = int(input('How much money would you like to play with? (no dollar sign) '))
    N = int(input('How many times would you like to play? '))
    print(calculate_UCB(balance, N))