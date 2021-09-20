#This script allows you to input your calorie needs and how much food you have already eaten, and outputs a food that would get you to your calorie needs for the day
# 
# Creator: Ben Sharrer
#
# Last Edited 9/20/21
# 

import sys, os, time, argparse

def calories_to_food(cal_needed):
    food = ''
    if cal_needed <= 0:
    	food = 'You have already met your calorie needs for the day'
    elif cal_needed <= 4:
    	food = 'You should eat an M&M'
    elif cal_needed <= 20:
    	food = 'Try half of a cucumber'
    elif cal_needed <= 50:
    	food = 'You could have 10 olives'
    elif cal_needed <= 100:
    	food = 'Have an apple'
    elif cal_needed <= 200:
    	food = 'You should drink half of a liter of Coke'
    elif cal_needed <= 350:
    	food = 'Maybe try a baked potatoe with some sour cream'
    elif cal_needed <= 500:
    	food = 'You could have some fried chicken to get to your goal'
    elif cal_needed <= 1000:
    	food = 'Try two-three hot dogs (depending on the toppings!)'
    elif cal_needed <= 2000:
    	food = 'A big mac, large fries, and McFlurry from Mcdonalds would fill you up!'
    else:
    	food = 'You still need a lot of calories to meet your goal. Try a couple meals!'
    return food

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gives you a food suggestion based on your caloric needs")
    parser.add_argument('input', type = int, help = "Input your daily calorie needs")
    total_cals = parser.parse_args()
    parser2 = argparse.ArgumentParser(description="Gives you a food suggestion based on your caloric needs")
    parser2.add_argument('input', type = int, help = "Input your daily calorie needs")
    total_cals = parser2.parse_args()
    print(calories_to_food(total_cals-eaten_cals))
