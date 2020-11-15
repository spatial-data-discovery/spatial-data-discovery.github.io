#Utility Script
#
#Hannah Slevin
#
#grade_calculator.py
#
#VERSION 2.0
#
#LAST EDIT: 2020-11-14
#
#The program will collect each percentage grade and turn them into points that
#sum up to 100 and output a final percentage and letter grade for the course.
#
#######################
#  REQUIRED MODULES   #
#######################
#
import argparse
#
############################
# Calculating Letter Grade #
############################
#Calculate letter grade based on grade distribution found in syllabus using a
#series of if statements
def LetterGrade(total_pcnt):
    """Calculate the final letter grade.

    Keyword arguments:
    total_pcnt -- the percentage grade calculated in the main frame
    """
    try:
        total_pcnt = float(total_pcnt)
    except:
        raise TypeError("Value must be input as an integer or float! Try again.")
    if total_pcnt > 93.0:
        print("Final Letter Grade: A")
        print("Congratulations on Superior Mastery!")
    elif (total_pcnt >= 90) & (total_pcnt <= 92.99):
        print("Final Letter Grade: A-")
    elif (total_pcnt >= 87) & (total_pcnt <= 89.99):
        print("Final Letter Grade: B+")
    elif (total_pcnt >= 83) & (total_pcnt <= 86.99):
        print("Final Letter Grade: B")
        print("Congratulations on Good Mastery!")
    elif (total_pcnt >= 80) & (total_pcnt <= 82.99):
        print("Final Letter Grade: B-")
    elif (total_pcnt >= 77) & (total_pcnt <= 79.99):
        print("Final Letter Grade: C+")
    elif (total_pcnt >= 73) & (total_pcnt <= 77.99):
        print("Final Letter Grade: C")
        print("Your performance is satisfactory")
    elif (total_pcnt >= 70) & (total_pcnt <= 72.99):
        print("Final Letter Grade: C-")
    elif (total_pcnt >= 67) & (total_pcnt <= 69.99):
        print("Final Letter Grade: D+")
    elif (total_pcnt >= 60) & (total_pcnt <= 66.99):
        print("Final Letter Grade: D")
        print("Unfortunately, your performance is less-than-satisfactory")
    elif total_pcnt <60:
        print("Final Letter Grade: F")
        print("Unfortunately, your performance is not satisfactory")
        print("You will need to retake this course")
#
############################
# Calculating Weights  #
############################
#This function calculates the weight of each assignment.
#It is called in the mainframe.
def Weight_Calc(points, weight):
    """Calculate the weights for each Assignment.

    Keyword arguments:
    points -- the number of points scored for each assignment
    weight -- the number of points that the assingment is worth out of 100
    """
    try:
        points = float(points)
        try:
            weight = float(weight)
            if (100 >= points >= 0):
                if (100 > weight > 0):
                    wt = (points/100)*weight
                else:
                    raise ValueError('Weight argument must be less than 100 and greater than 0.')
            else:
                raise ValueError('Points argument must be less than or equal to 100 and greater than or equal to 0.')
        except:
            raise TypeError('Input must be a float or integer')
    except:
            raise TypeError('Input must be a float or integer')
    return wt

#
###################
#      Main       #
###################
if __name__ == '__main__':
    # --help command line description
    parser = argparse.ArgumentParser(
    description = "This script will calculate your final grade based on the percentage grades that you input for each assignment.")
    args = parser.parse_args()
    ################################
    # Calculating Percentage Grade #
    ################################
    #This program will calculate your Semester grade based on entering percentages from each assingment
    #
    #Create a list to store each grade
    grades = []
    #
    #
    #Section one
    print('Section 1: Discussion Grade')
    #
    #Collect discussion grade as discuss, apply weight, and append to grades list
    discuss = input("Enter percentage grade for your Discussion Meetings: ")
    discuss = Weight_Calc(discuss, 24)
    grades.append(discuss)
    #
    #
    #Section two
    print('Section 2: Assignments')
    #Collect grade, apply weight, and append to grades list
    atc = input("Enter percentage grade for the About the Coder assingment: ")
    atc = Weight_Calc(atc, 5)
    grades.append(atc)
    #
    #Collect utility script grade as us, apply weight, and append to grades list
    us = input("Enter percentage grade for the Utility Script assingment: ")
    us = Weight_Calc(us, 5)
    grades.append(us)
    #
    #Collect sparse data grade as sdc, apply weight, and append to grades list
    sdc = input("Enter percentage grade for the Sparse Data Challenge assingment: ")
    sdc = Weight_Calc(sdc, 5)
    grades.append(sdc)
    #
    #Collect conversion scripts grade as cs, apply weight, and append to grades list
    cs = input("Enter percentage grade for The Conversion Scripts assingment: ")
    cs = Weight_Calc(cs, 10)
    grades.append(cs)
    #
    #Collect PEP 8 script grade as pep8, apply weight, and append to grades list
    pep8 = input("Enter percentage grade for The PEP8 assingment: ")
    pep8 = Weight_Calc(pep8, 5)
    grades.append(pep8)
    #
    #
    #Section three
    print('Section 3: Reports')
    #Collect weekly reports grade as reports, apply weight, and append to grades list
    reports = input("Enter percentage grade for your reports: ")
    reports = Weight_Calc(reports, 24)
    grades.append(reports)
    #
    #
    #Section four
    print('Section 4: Project')
    #Collect project grade as proj, apply weight, and append to grades list
    proj = input("Enter percentage grade for your project: ")
    proj = Weight_Calc(proj, 22)
    grades.append(proj)
    #
    #Calculate the sum of points for each assignment, since the point totals add up to 100,
    #there is no need to divide by a total
    total_pcnt = sum(grades)
    print("Final Grade (in percentage points):",round(total_pcnt,3),"%")
    #
    ################################
    # Print Letter Grade #
    ################################
    LetterGrade(total_pcnt)

