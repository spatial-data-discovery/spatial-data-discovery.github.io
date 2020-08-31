# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 18:44:30 2020

@author: jandj
"""

##
# This is a Python utility script for Spatial Data Discovery, created by Jonah Casale.
# This script calculates your caloric needs based on height, age, sex, and weight.
##

# Imports here
import argparse

# First determine the person's BMR using Harris-Benedict formula.
# Adult male: 66 + (6.3 x body weight in lbs.) + (12.9 x height in inches) - (6.8 x age in years) = BMR
# Adult female: 655 + (4.3 x weight in lbs.) + (4.7 x height in inches) - (4.7 x age in years) = BMR 
userBodyWeight = input("Please enter your body weight (lbs.): \n")
userHeight = input("Please enter your height (in inches): \n")
userSex = input("Please enter your sex: type M for male or F for female: \n")
userAge = input("Please enter your age (in years): \n")
# Cast all the numerical inputs to floats.
userBodyWeight = float(userBodyWeight)
userHeight = float(userHeight)
userAge = float(userAge)
# Check if user's inputs are positive, not negative.  If negative, print error message.  
# Otherwise, program continues.
if (float(userBodyWeight) < 0) or (float(userHeight) < 0) or (float(userAge) < 0) :
    print("One of your answers is a negative number.  Please enter positive numbers only.  Try again.")
else :
    # Determine formula based on sex to calculate BMR.
    if (userSex == "M") or (userSex == "m") :
        userBMR = 66 + (6.3 * userBodyWeight) + (12.9 * userHeight) - (6.8 * userAge) 
    if (userSex == "F") or (userSex == "f") :
        userBMR = 655 + (4.3 * userBodyWeight) + (4.7 * userHeight) - (4.7 * userAge) 
        
    # Now ask for user's activity level.
    print("Would you say that you are: \n")
    print("sedentary (little or no exercise at all)")
    print("lightly_active (light exercise/sports 1-3 days/week)")
    print("moderately_active (moderate exercise/sports 3-5 days/week)")
    print("very_active (hard exercise/sports 6-7 days a week)")
    print("extremely_active (we're talking elite athletes here!)")
    
    activityLevel = input("Please type your activity level (sedentary, lightly_active, moderately_active, very_active, extremely_active): \n")
    
    if activityLevel == "sedentary" :
        caloricNeeds = userBMR * 1.2
    elif activityLevel == "lightly_active" :
        caloricNeeds = userBMR * 1.375
    elif activityLevel == "moderately_active" :
        caloricNeeds = userBMR * 1.55
    elif activityLevel == "very_active" :
        caloricNeeds == userBMR * 1.725
    elif activityLevel == "extremely_active" :
        caloricNeeds == userBMR * 1.9
    else :
        print("You inputed your activity level incorrectly.  Start over and try again.")
        
    print(" ")
    print("Based on the information you have inputted, your APPROXIMATE caloric needs are " + str(caloricNeeds) + " calories per day to maintain your current weight.")
    
    
p = argparse.ArgumentParser(description="Calculates your daily caloric needs")