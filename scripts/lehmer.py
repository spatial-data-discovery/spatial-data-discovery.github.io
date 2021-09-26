# lehmer.py

# By: Minkyong Song

# Version 1.0

# Last Edit: 2021-09-24

# Calculates all full-period multipliers between number 1 to m, which the user will select.
# Full-period multiplier is a number indicated as 'a' which you will get all numbers between 1 and m-1,
# when you calculate the lehmer algorithm, ax mod m, for m-1 times.
# The lehmer algorithm is used to explain random number generator
# because it returns all number between 1 and m-1 randomly when you chose a different seed, x.


##############################################################################
#                                 FUNCTIONS                                  #
##############################################################################
def lehmer_full_period_multiplier(a, m):
  '''
  This function returns multiplier 'a' if the Lehmer Algorithm g(x) = ax mod m returns a full period
  '''

  # List to save the number randomly number generated according to the Lehmer Algorithm
  random = list()

  # Set the seed x as 1
  x = 1
  # Go through Lehmer Algorithm m - 1 times
  for i in range(1, m):
    # Calculate ax mod n and append it to the list
    ax = a * x
    x = ax % m
    random.append(x)

  # If the list of randomly generated number has all number from 1 ~ m, return the multiplier 'a'
  if set(random) == set(range(1, m)):
    return(a)

def all_full_period_multiplier(m):
  '''
  This function returns all full-period multiplier as a list.
  The full period multipliers are calculated using lehmer_full_period_multiplier.
  '''
  # List to save full period multiplier
  full_period_multiplier = list()

  # Go through lehmer_full_period_multiplier in between 2 and l.
  # 1 was excluded because ax will be 1 * 1, which will give 1 for every mod.
  # Thus, 1 cannot be a full-period full-period multiplier in any case.
  for i in range (2, m):
    a = lehmer_full_period_multiplier(i, m)

    # If the number between 2 and m is a full-period multiplier, append to the list
    if a:
      full_period_multiplier.append(a)

  return full_period_multiplier


##############################################################################
#                                   MAIN                                     #
##############################################################################

if __name__ == "__main__":

  # Get input from the user
  # If the input is not an integer, make the user try again
  while True:
        try:
            m = int(input("\nEnter the multiplier: "))
        except ValueError:
            print("\nSorry, I only accept integer. Please try again.")
        else:
            break

  # Calculate and get all full-period multiplier of m
  full_period_multiplier = all_full_period_multiplier(m)
  
  # Print the answers
  print("\nAll full-period multipliers: ", full_period_multiplier)
  print("\nThe number of all full-period multipliers: ", len(full_period_multiplier))

  # If there is any multiplier print the min and max full-period multiplier
  if len(full_period_multiplier) != 0:
    print("The smallest full-period multipliers: ", min(full_period_multiplier))
    print("The smallest full-period multipliers: ", max(full_period_multiplier), '\n')
  # If there is no multiplier, print that there is no full-period multiplier
  else:
    print("There is no full-period multipliers\n")