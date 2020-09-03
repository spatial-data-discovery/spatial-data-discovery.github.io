#Calculate Course grade
#Hannah Slevin
#
#grade_calculator.py
#
#VERSION 1.0
#
#LAST EDIT: 2020-09-03
#
#This code requires users to input their percentage grade for each of the graded course assingments without the percentage sign.
#The program will collect each percentage grade and turn them into points that sum up to 100 and output a final percentage and letter grade for the course.
#
#######################
#  REQUIRED MODULES   #
#######################
import argparse

################################
# Calculating Percentage Grade #
################################

#This program will calculate your Semester grade based on entering percentages from each assingment
#
#Create a list to store each grade
grades = []
#
#Before each section a line will print distinguishing which section of the grade is being taken as an input
#
#Print section one
print('Section 1: Discussion Grade')
#
#The user is prompted to enter their discussion grade
#The script casts it as an int and assigns the integer to variable "discuss"
discuss = int(input("Enter percentage grade for your Discussion Meetings: "))
#discussion grade percentage is changed to point value
discuss = (discuss/100)*24
#discussion grade is appended to the grade list
grades.append(discuss)
#
#
#Print Section two
print('Section 2: Assignments')
#
#The user is prompted to enter their About the coder assignment grade
#The script casts it as an int and assigns the integer to variable "atc"
atc = int(input("Enter percentage grade for the About the Coder assingment: "))
#The about the coder grade percentage is changed to point value
atc = (atc/100)*5
#The about the coder grade is appended to the grade list
grades.append(atc)
#
#The user is prompted to enter their Utility Script assignment assignment grade
#The script casts it as an int and assigns the integer to variable "us"
us = int(input("Enter percentage grade for the Utility Script assingment: "))
#The utlity script grade percentage is changed to point value
us = (us/100)*5
#The utility script grade is appended to the grade list
grades.append(us)
#
#The user is prompted to enter their Sparse Data Challenge Assignment grade
#The script casts it as an int and assigns the integer to variable "sdc"
sdc = int(input("Enter percentage grade for the Sparse Data Challenge assingment: "))
#The sparse data challenge grade percentage is changed to point value
sdc = (sdc/100)*5
#The sparse data challenge grade is appended to the grade list
grades.append(sdc)
#
#The user is prompted to enter their Conversion Scripts Assignment grade
#The script casts it as an int and assigns the integer to variable "cs"
cs = int(input("Enter percentage grade for The Conversion Scripts assingment: "))
#The conversion scripts grade percentage is changed to point value
cs = (cs/100)*10
#The conversion scripts grade is appended to the grade list
grades.append(cs)
#

#The user is prompted to enter their The PEP8 Assignment grade
#The script casts it as an int and assigns the integer to variable "pep8"
pep8 = int(input("Enter percentage grade for The PEP8 assingment: "))
#The PEP8 grade percentage is changed to point value
pep8 = (pep8/100)*5
#The PEP8 grade is appended to the grade list
grades.append(pep8)
#
#
#Print Section three
#The user is prompted to enter their reports grade
#The script casts it as an int and assigns the integer to variable "reports"
print('Section 3: Reports')
reports = int(input("Enter percentage grade for your reports: "))
#The reports grade percentage is changed to point value
reports = (reports/100)*24
#The reports grade is appended to the grade list
grades.append(reports)
#
#
#Print Section four
print('Section 4: Project')
#The user is prompted to enter their project grade
#The script casts it as an int and assigns the integer to variable "proj"
proj = int(input("Enter percentage grade for your project: "))
#The project grade percentage is changed to point value
proj = (proj/100)*22
#The project grade is appended to the grade list
grades.append(proj)
#print(grades) #uncomment to check that program correctly appended grades to grade list
#
#Calculate the sum of points for each assignment, since the point totals add up to 100, there is no need to divide by a total
total_pcnt = sum(grades)
#Print final perentage grade
print("Final Grade (in percentage points):",total_pcnt,"%")
#
#
############################
# Calculating Letter Grade #
############################
#Calculate letter grade based on grade distribution found in syllabus using a series of if statements
#If the user scores over 93%, print A & a message
if total_pcnt > 93.0:
    print("Final Letter Grade: A")
    print("Congratulations on Superior Mastery!")
#If the user scores between 90% and 92.99%, print A-
elif (total_pcnt >= 90) & (total_pcnt <= 92.99):
    print("Final Letter Grade: A-")
#If the user scores between 87% and 89.99%, print B+
elif (total_pcnt >= 87) & (total_pcnt <= 89.99):
    print("Final Letter Grade: B+")
#If the user scores between 83% and 86.99%, print B & a message
elif (total_pcnt >= 83) & (total_pcnt <= 86.99):
    print("Final Letter Grade: B")
    print("Congratulations on Good Mastery!")
#If the user scores between 80% and 82.99%, print B-
elif (total_pcnt >= 80) & (total_pcnt <= 82.99):
    print("Final Letter Grade: B-")
#If the user scores between 77% and 79.99%, print C+
elif (total_pcnt >= 77) & (total_pcnt <= 79.99):
    print("Final Letter Grade: C+")
#If the user scores between 73% and 77.99%, print C & a message
elif (total_pcnt >= 73) & (total_pcnt <= 77.99):
    print("Final Letter Grade: C")
    print("Your performance is satisfactory")
#If the user scores between 70% and 72.99%, print C-
elif (total_pcnt >= 70) & (total_pcnt <= 72.99):
    print("Final Letter Grade: C-")
#If the user scores between 67% and 69.99%, print D+
elif (total_pcnt >= 67) & (total_pcnt <= 69.99):
    print("Final Letter Grade: D+")
#If the user scores between 60% and 66.99%, print D & a message
elif (total_pcnt >= 60) & (total_pcnt <= 66.99):
    print("Final Letter Grade: D")
    print("Unfortunately, your performance is less-than-satisfactory")
#If the user scores under 60%, print F & a message
elif total_pcnt <60:
    print("Final Letter Grade: F")
    print("Unfortunately, your performance is not satisfactory")
    print("You will need to retake this course")

###################
#      Main       #
###################
if __name__ == '__main__':
    # --help command line description
    parser = argparse.ArgumentParser(
    description = "This script will calculate your final grade based on the percentage grades that you input for each assignment.")
    args = parser.parse_args()
