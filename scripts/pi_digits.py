# This ended up being way easier than I thought
#Many classes/assignemnts use differnt approximations for pi so this is a script to easily be able to achive any approximation of pi. 
#tested all the way out to 1,000,000 digits
#this starts counting at 1 rather than 0 so if you do pi_digets(1) it will give you pi with 1 decimal place. If you do pi_digets(0) it will give you pi with 0 decimal places. 

#import the the library we need
from mpmath import mp

#define the function
def pi_digets(x):
  mp.dps = x+1 #make it so that it will give you the number of decimal places you imput
  if str(x).isnumeric() == True: #check to see if you made a valid imput 
    return print(mp.pi) #print the correct value
  else:#if invalid 
    return print('You did not imput an int for x')