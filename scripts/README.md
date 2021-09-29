# README
--------
* LAST UPDATED: 2019-10-24
* ORGANIZATION: spatial-data-discovery
* REPOSITORY: spatial-data-discovery.github.io/scripts

# DESCRIPTION
This folder contains utility scripts as well as a selection of data files necessary for running certain scripts.

## Data Files

### american
* Line-separated words (>300k); this data file is needed for hangman.py.

### mbox-short.txt
* Data file for testing first_word_counter.py.

### oldchangelog.txt
* Empty file for starting changelog_generator.py.

### test_ranking_calculater.csv
* A test csv file for rankings calculator.py.

### text.txt
* A test file for random_caps.py.


## Script Files

### barchart_generator.py
* This script takes a .csv file and generates a barchart as a .png. It allows the user to specify the columns for the x and y axes. Saves .png in working directory.

### Book_keeping.py
* This script takes in two excel files and compares them to update inventory.  

### build_madden_roster.py
* This script builds a randomized full roster of NFL players in Madden 22.

### caesar_cipher.py
* This script takes a message given by the user and encrypts it using a Caesar Cipher

### change_calculator.py
* This script determines the simplest way to generate exact change of a given number of cents (represented by an integer), using quarters, dimes, nickels, and pennies. Will generate an error if the given number of cents is negative or not an integer.

### changelog_generator.py
* This script generates a changelog (Hopefully) to the professors specs programmatically; it requires a PowerShell script (p.ps1) and an old change log (oldchangelog.txt).

### crosswind.py
* This script determines which runway pilots should use based on runways available, wind direction, and wind speed.

### dad_joke_emailer.py
* This script emails you one dad joke using your email to send and receive the message.

### darts.py
* This script is a throwing darts game that lets the user choose how many darts to throw at a circular dart board and tell them what percent of the darts landed on the board.

### dna_translator.py
* This script takes a DNA sequence, finds the complementary sequence (called the template DNA), and returns the corresponding RNA codons and proteins they encode for in a list.

### embassy_news_scraper.py
* This script takes a url of a news source from one of Chinese embassy websites and extracts its description.

### extract_column.py
* This script takes a csv file and an option argument -c for which column needs to be extracted from the file. It will output a text file containing the column without the header.

### file_remover.py
* This script takes in the path to a directory from which you want to delete all
files of a certain type and what that type/extension is (e.g. .py or .ini) and
removes all files of that type within that directory.

### first_word_counter.py
* This script takes .txt or .md files and a word of your choice and returns each sentence/sentences where the specified word is the first word.
    Test using mbox-short.txt.

### grade_calculator.py
* This script takes each grade from the Spatial Data Discovery course as a user input and outputs a final percentage and letter grade.

### hangman.py
* This script uses the dictionary, american, to play Hangman in command prompt.

### hanoi.py
* This script takes the number of rings as an input, and then plays/solves the puzzle Tower of Hanoi

### hdf_qgis.py
* This script opens a MODIS HDF4 file using GDAL, converts it to a GeoTIFF, and opens it for visualization in QGIS (tested using QGIS 3.4).

### hdf_read.py
* This script opens and reads an HDF5 file using h5py.

### hdf_write.py
* This script creates a new and edits an existing HDF5 file using h5py.

### image_merger.py
* This script allows users to select image files (supports most file types) from their computer,
  organize them, and then merge them into a multi-page PDF.

### josephus.py
* This script demonstrates the way linked lists work as well as adding a fun game to the mix!
  Josephus takes any number inputted by the user and makes a linked list of 1 to that number.
  It will then rotate the linked list so the first value becomes the last and then removes the new first value.
  It will continue to do this until there is only one number left.
  This is the survivor!

### keywords.py
* This script takes a text file, get the most commonly used words, and then googles for links related to these words.

### live_aviation.py
* This script retrieves live aviation data from an opensource API, and then allows the user to save said file to their machine.

### magic8ball.py
* This script asks the user a question and then gives them the response a Magic 8 ball would.

### make_art.py
* This script uses TensorFlow's DeepDream model to create whimsical artwork out of a user-provided image by enhancing patterns detected within the picture.  Note: This file should be run in a Python notebook environment (works well in both Jupyter and Google Colab, which offers GPU run-time capabilities).  The way the file has been written thus far only allows the input and output image to be displayed within Python notebooks, and the images will not be visibly displayed when running as a typical, stand-alone script.

### milkweed_data.py
* This script takes a .csv file of morphological data from three different species of milkweed: Asclepias exaltata, Asclepias syriaca, and Asclepias speciosa.
* The script also conducts a principal component analysis using 6 appropriately scaled variables: leaf width, leaf length, basal angle, tip angle, ratio of petiole to tip, ratio of length by width.

### movie_script_scraper.py
* This code scrapes movie scripts from Scripts.com and saves the text in a .txt file.

### music_randomizer.py
* This script randomizes and organizes MP3 files in a folder or on a USB drive.

### nc_read.py
* This script reads attributes, variables, and dimensions from a NetCDF "classic" data file using scipy.io.

### nc_write.py
* This script creates a NetCDF "classic" data file and writes attributes, variables, and dimensions to the file using scipy.io.

### netCDF_mean.py
* This script reads in a netCDF file and writes out the average of the variables to a new file.

### nthPrime.py
* This is a simple CLI script takes an integer input from the user, and outputs the nth Prime number. (1=2,2=3,3=5,4=7,...)

### numberconverter.py
* This script takes in a decimal integer and converts it into binary, octal, and hexadecimal formats.

### parsehtml.py
* this script parses a page from packhacker.com to get all the text (with tag <p>), and saves it to txt file, e.g. https://packhacker.com/travel-gear/heimplanet/neck-pouch-a5/

### Pdf_Converter.py
* This script converts files between different formats.
    It is currently hardcoded to convert .docx to .pdf.

### PlotRGB.py
* This script prompts the user for the path to a folder containing Landsat 5 bands and the function plots a natural color image of the satellite image and prints some basic information about the data.

### random_caps.py
* This script takes a text file of ASCII characters, randomly capitalizes them, and writes them out to a new text file.
    
### randomPassword.py
* Generates a password of a given length, with a default length of 10

### ranking_calculator.py
* This script calculates the ranking of a list of players/students (or anything you want to rank) based on their scores.

### README.md
* This readme file.

### rename.py
* This script renames files in a folder based on a regular expression.
    The script is set to rename all files of a given type by replacing an underscore (\_) in the filename with a hyphen (-).

### sentiment_analysis.py
* This script conducts sentiment analysis, assessing subjectivity and polarity of text data stored in a .csv file.

### simplified_roulette.py
* This script simulates a simplified (only color bets and straight bets) version of roulette with three different roulette wheels (No Zero, French/Single Zero, and American/Double Zero).

### slot_machine.py
* This script simulates how upper confidence bound reinforcement learning works with a slot machine and prompts the user for the beginning balance and how many times to play.

### spreadsheet_cleaner.py
* This script removes leading, trailing, and double whitespace from Excel spreadsheets.

### statistical_overview.py
* Prints a statistical overview of numerical data read in through a text file.
    
### text_preprocessing.py
* This script cleans text by lowercasing; removing stop words, punctuation, and numbers; and performing tokenization and lemmatization.

### twoSum.py
* Finds the index of two values in a list that adds up to the target number

### webscraper.py
* This script takes the url for the WM CS website and extracts info about the department and courses offered.

### what_to_watch.py
* This script takes movie or show titles input by the user and outputs one for the user to watch next. The user is also given the option to re-pick.

### word_bank.py
* This script creates a word bank of all unique words in inserted sentence.
    
### script.py
* This script stitches together two or more images that have overlapping areas. 
