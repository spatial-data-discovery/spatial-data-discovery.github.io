import argparse


def change(amount):
    if amount < 0:
        raise ValueError('It\'s impossible to have a negative number of cents. Please try again.')
    #The amount can't be negative

    change_count = dict(); #This dictionary keeps track of the number of each American coin
    quarters = int(amount/25)
    amount-=(quarters * 25)
    dimes = int(amount/10)
    amount-=(dimes * 10)
    nickels = int(amount/5)
    amount-=(nickels * 5)
    pennies = amount

    change_count['Quarters'] = quarters
    change_count['Dimes'] = dimes
    change_count['Nickels'] = nickels
    change_count['Pennies'] = pennies
    return change_count

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the combination of the smallest number of common American coins (quarters, dimes, nickels, and pennies) that add up to the given number of cents. The number of cents needs to be represented by an integer and must be positive.')
    parser.add_argument('amount', type=int, help="The total number of cents (integer)")
    args = parser.parse_args()
    print("The number of quarters, dimes, nickels, and pennies needed to generate exact change: ", change(args.amount))
