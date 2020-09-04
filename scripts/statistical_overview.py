#Created by Jamil Abbas

#09-03-2020

#This is a simple script that takes in a text file populated with numbers and returns a statistical overview

###########################
#Required Modules
###########################
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import stats
import argparse


def print_fxn(numbers_array):
    print("N=", len(numbers_array), "\n") #Number of variables N

    print ("Mean:" , np.mean(numbers_array), "\n") #Mean of the data

    print("Median: " , np.median(numbers_array) , "\n") #Median of the data

    mode_info = sp.stats.mode(numbers_array)
    print("Mode: " ,mode_info[0] , "\n") #Mode of the data

    print("Variance:" , np.var(numbers_array), "\n") #Variance of the data

    print("Standard Deviation:" , np.std(numbers_array), "\n") #Standard deviation of the data

    print("Skewness:" , sp.stats.skew(numbers_array), "\n") #Skewness of the data

    print("Kurtosis:" , sp.stats.kurtosis(numbers_array), "\n") #Kurtosis of the data




if __name__ == "__main__":

    p = argparse.ArgumentParser(description="Prints a statistical overview of numerical data read in through a text file.")
    args = p.parse_args()


    filename = input("Enter the Path to the File:")
    with open(filename) as f:
        numbers = [int(x) for x in f.read().split()]

    numbers_np = np.array(numbers)

    print_fxn(numbers_np)

    _ = plt.hist(numbers_np)
    _ = plt.xlabel("Range")
    _ = plt.ylabel("Frequency")
    plt.show()
