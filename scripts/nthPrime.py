#Written for Python 3.9 64-bit

import time
import math

#Lets user define 'n', the neth prime number to be calculated

def floatLoop():
    while True:
        print("Please enter \'n\', to find the nth prime number. Enter \'q\' to terminate the program.")
        userinput = input(" > ")
        if userinput.lower() == "q" or userinput.lower() == "quit":
            exit(1)
        try:
            if float(userinput) != int(userinput):
                print("||ERROR|| Invalid integer")
            elif int(userinput) < 1:
                    print("||ERROR|| Integer must be greater than 0")
            else:
                return int(userinput)
        except:
            print("||ERROR|| Invalid integer")

while True:
    #Discovers the nth prime number though smart brute-force
    n = floatLoop()
    start = time.time_ns()

    cur = 2
    curindex = 1
    while curindex < n: #Brute-forces through all the integers
        cur += 1
        prime = True
        divisor = 2
        for i in range (2, math.ceil(cur**0.5)+1):    #For every integer between 2 and the square root of the current number...
            if cur / divisor == math.floor(cur / divisor): #If the quotient is equal to the floor of the quotient, the divisor is perfect, the number is not prime. Skip to the next number
                prime = False
                break
            else:
                divisor += 1
        if prime:    #If we discovered a prime number, iterate the current prime index
            curindex += 1

    time_ms = (time.time_ns() - start)/1000000

    #Prints the results of the calculation. Have to do some malarkey to make sure that the grammar is right for "1st, 21st, 11th, 111th, etc."

    lastdigit = str(n)[len(str(n))-1]
    last2digits = str(n)[len(str(n))-2:len(str(n))]
    if lastdigit == "1" and last2digits != "11":
        print("The " + str(n) + "st prime number is " + str(cur))
    elif lastdigit == "2" and last2digits != "12":
        print("The " + str(n) + "nd prime number is " + str(cur))
    elif lastdigit == "3" and last2digits != "13":
        print("The " + str(n) + "rd prime number is " + str(cur))
    else:
        print("The " + str(n) + "th prime number is " + str(cur))

    print("Discovered in " + str(time_ms) + "ms\n")

