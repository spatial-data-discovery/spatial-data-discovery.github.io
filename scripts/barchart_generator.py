# barchart_generator.py

# By: Sylvia Shea

# Version 1.0

# Last Edit: 2020-09-03

# Purpose: This script takes a .csv file and allows the 
# user to specify the x and y variables to be plotted.
# It saves the figure as a .png. 

import matplotlib.pyplot as plt
import pandas as pd
import argparse
import sys

def generate_barchart(df,x_col,y_col,title):
    fontname = 'Sathu'
    color = 'cornflowerblue'
    # Fig specs
    fig, ax = plt.subplots()
    ax.set_ylabel(y_col,fontsize=16,fontname=fontname)
    ax.set_xlabel(x_col,fontsize=16,fontname=fontname) 
    ax.tick_params(axis='x',labelsize=12)
    ax.tick_params(axis='y',labelsize=12)
    for i in ['top','right']:
        ax.spines[i].set_visible(False)
    # Bar plot 
    ax.bar(x=df[x_col], height=df[y_col], color=color)
    ax.set_title(title,fontsize=20,fontname=fontname)
    plt.savefig(title, bbox_inches='tight', dpi=1000)


def main():    
    res = 'y'
    while res == 'y':
        sys.stdout.write('Input CSV name (include .csv) ')
        sys.stdout.flush()
        path = input()

        try: 
            df = pd.read_csv(path)
        except FileNotFoundError:
            print('File not found!')

        sys.stdout.write('Here are your columns: ')
        print('\n---------------------------')
        columns = list(df.columns)
        [print(str(i + 1) + ': ' + col) for i,col in enumerate(columns)]
        sys.stdout.write('Input number for x value ')
        sys.stdout.flush()
        x_key = int(float(input())) - 1
        x_col = columns[x_key]

        sys.stdout.write('Input number for y value ')
        sys.stdout.flush()
        y_key = int(float(input())) - 1
        y_col = columns[y_key]

        sys.stdout.write('Input title')
        title = str(input())

        # Plot 
        print('\n-------------------'
                'Generating Plot'
                '-------------------')
                # must fix group and add proc inputs here
        generate_barchart(df,x_col,y_col,title) 
        print('\n-------------------'
                'Plot Generated!'
                '-------------------')
        sys.stdout.write('\nContinue? (y/n): ')
        sys.stdout.flush()
        res = input()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make a barchart from CSV')
    args = parser.parse_args()
    main()