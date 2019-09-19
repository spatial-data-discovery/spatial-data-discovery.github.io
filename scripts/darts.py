import random
import math

#FUNCTIONS
#Help function from Davis's music randomizer
def show_help():
    """
    Name:     show_help
    Inputs:   None
    Outputs:  None
    Features: Prints the help text when user uses the '-h' command flag
    """
    help_txt = ( "-h, --help   Enter a whole number!\n")
    print(help_txt)

#VARIABLES

#total darts thrown
n = input('How many darts would you like to throw?')
if n == '-h' or n == '--help':
  show_help()
else:
  try:
    total = int(n)
    if total < 0:
      print('You must must throw a positive number of darts.')
    #Number of darts that land inside (initializing the list)
    inside = 0
    #Total number of darts to throw (gotten from input)
    # total = n
    #Define the length of a side of the square
    length = 10
    #Define the size of the circle, originating from the center of the square
    circle_radius = 5.0

    #Iterate for the number of darts
    for i in range(0, total):
      x = random.uniform(0, length)
      y = random.uniform(0, length)
      #test if the dart is inside or outside
      #(ie, is the distance from the center of the square less than the circle radius?)
      if math.sqrt((x**2) + (y**2)) < circle_radius*2:
        inside += 1

    print("Percent of Darts Inside:")
    print((inside / total)* length**2)

  except ValueError:
    print('Bad!')
