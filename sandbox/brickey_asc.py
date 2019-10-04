# Morgan Brickey
#
# raster.py
#
# This script takes a raster file and checks that the number of rows and columns
# are correct, and that all data inputs are numeric
# Last edited 10/03/19

# Required Modules
import os
import pandas as pd
import re

# filepath = '/Users/MorganBrickey/Documents/Repositories/spatial_data_discovery/spatial-data-discovery.github.io/sandbox/brickey.txt'


# Initialize constants
NCOLS = 0
NROWS = 0
XLLCORNER = 0
YLLCORNER = 0
XLLCENTER = 0
YLLCENTER = 0
CELLSIZE = 0
NODATAVALUE = 0
NODATA_VALUE = 0

# Initialize two empty lists
new = []
data = []

# Open the file
# enumerate used in for loop
# Look for the constants in line, use re.findall to return matches of just numbers, including negatives and decimals
# Find the first item in the list, convert to integer and assign it to constant
# if no constant is in the line, add the line to data list
# References: https://stackabuse.com/read-a-file-line-by-line-in-python/
#             https://docs.python.org/2/library/re.html


def findFile(filepath):
    with open(filepath) as fp:
        # read the file line by line
        for cnt, line in enumerate(fp):
            print(line)
            if 'NCOLS' in line:
                # finds all numbers, assigns first number as variable
                ncols = (re.findall('\-?\d+', line))
                NCOLS = int(ncols[0])
            elif 'NROWS' in line:
                nrows = (re.findall('\-?\d+', line))
                NROWS = int(nrows[0])
            elif 'XLLCORNER' in line:
                xcorner = (re.findall('\-?\d+(?:\.\d+)?', line))
                XLLCORNER = float(xcorner[0])
            elif 'YLLCORNER' in line:
                ycorner = (re.findall('\-?\d+(?:\.\d+)?', line))
                YLLCORNER = float(ycorner[0])
            elif 'XLLCENTER' in line:
                xcenter = (re.findall('\-?\d+(?:\.\d+)?', line))
                XLLCENTER = float(xcenter[0])
            elif 'YLLCENTER' in line:
                ycenter = (re.findall('\-?\d+(?:\.\d+)?', line))
                YLLCENTER = float(ycenter[0])
            elif 'CELLSIZE' in line:
                cellsize = (re.findall('\-?\d+', line))
                CELLSIZE = float(cellsize[0])
            elif 'NODATA_VALUE' in line:
                nodata = (re.findall('\-?\d+', line))
                NODATA_VALUE = float(nodata[0])
            elif 'NODATAVALUE' in line:
                nodata = (re.findall('\-?\d+', line))
                NODATAVALUE = float(nodata[0])
            else:
                line = line.strip()
                if line != '': data.append(line)
            line = line.strip()
            new.append(line)
        

    # Check that NROWS is the right value by comparing it to length of data
    if len(data) != NROWS:
        print("FAILED: NROWS value does not match number of rows given")
    
    # Split values up in data by blank spaces
    for x in range(0, len(data)):
        data[x] = data[x].split(" ")

    # Check that NCOLS is the right value by comparing it to each item in data
    for x in range(0, len(data)):
        if len(data[x]) != NCOLS:
            print("FAILED: NCOLS value does not match number of columns given" , x)

    # make sure data is all numeric by using isdigit
    for x in range(0, NROWS):
        for j in range(0, NCOLS):
            if data[x][j].isdigit() == False:
                print("Error: Raster data can only be numeric")


if __name__ == '__main__':
    #open the file
    filepath = input('Enter filepath')
    
    if filepath.endswith('.txt' or '.asc' or ''):
            findFile(filepath)
    else:
            print("Wrong file type")