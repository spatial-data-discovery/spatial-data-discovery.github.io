#!/usr/bin/env python
"""
Gets all of the content that is in the first column of a csv
Skips the header to make content more iterable

Usage: Extract_header_column.py <Directory of files>
Output: Text files of the gene names in the same directory

Example output file name:
<Sib_18_30_symmetric_difference_results.csv_names
"""
import sys, csv, os, argparse

def main(fName,column,dirName = None):
	#with open(dirName + fName, 'r') as reader:
	with open(fName, 'r') as reader: 
		data = [row for row in csv.reader(reader)]

	#with open(dirName + fName + '_names.txt', 'w') as writer:
	with open(fName + '_names.txt', 'w') as writer:
		count = 0
		for row in data:
			if (count != 0):
				writer.write(row[column] + '\n')
			count += 1
	print("Wrote", count, "rows")


""" 
#this function is used if you want to run on a directory
def runOnDir(dirName):
	filenames = next(os.walk(dirName))[2]
	for fName in filenames:
		#if ('DESeq2') in fName:     #commented line out in case file name does not have DESeq in name
			print("Running on file:",  fName)
			main(fName, dirName)
"""


if __name__ == "__main__":
	"""
	dirName = sys.argv[1]
	if (dirName[-1] != '/'):
		dirName += '/'
	runOnDir(dirName)
	"""

	#this is used if you want to prompt the user for a specific column
	#inputNum = input("Which column number do you want to output?")
	p = argparse.ArgumentParser(description="Extracts the first (on default), or a given column from a csv file. This will output a new text file with _name at the end.")
	p.add_argument('file', nargs='?', help="The file path")
	p.add_argument("-c", "--column", type =int, default=0, help="The column number (starting at 0) that you want to be extracted.")
	args = p.parse_args()
	#fName = sys.argv[1]    #without argsparse
	main(args.file,args.column)


