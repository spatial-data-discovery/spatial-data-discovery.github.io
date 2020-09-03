# README
--------
* LAST UPDATED: 2019-10-24
* ORGANIZATION: spatial-data-discovery
* REPOSITORY: spatial-data-discovery.github.io/scripts

## DESCRIPTION
This folder contains utility and general functionality scripts.

## Files

### american
* Line-separated words (>300k); this data file is needed for hangman.py.

### Book_keeping.py
* This script takes in two excel files and compares them to update inventory.  

### caesar_cipher.py
* This script takes a message given by the user and encrypts it using a Caesar Cipher

### changelog_generator.py
* This script generates a changelog (Hopefully) to the professors specs programmatically; it requires a PowerShell script (p.ps1) and an old change log (oldchangelog.txt).

### crosswind.py
* This script determines which runway pilots should use based on runways available, wind direction, and wind speed.

### darts.py
* This script is a throwing darts game that lets the user choose how many darts to throw at a circular dart board and tell them what percent of the darts landed on the board.

### dna_translator.py
* This script takes a DNA sequence, finds the complementary sequence (called the template DNA), and returns the corresponding RNA codons and proteins they encode for in a list.

### embassy_news_scraper.py
* This script takes a url of a news source from one of Chinese embassy websites and extracts its description.

### extract_column.py
* This script takes a csv file and an option argument -c for which column needs to be extracted from the file. It will output a text file containing the column without the header.

### first_word_counter.py
* This script takes .txt or .md files and a word of your choice and returns each sentence/sentences where the specified word is the first word.
    Test using mbox-short.txt.
    
### grade_calculator.py
* This script takes each grade from the Spatial Data Discovery course as a user input and outputs a final percentage and letter grade.

### hangman.py
* This script uses the dictionary, american, to play Hangman in command prompt.

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

### mbox-short.txt
* Data file for testing first_word_counter.py.

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

### oldchangelog.txt
* Empty file for starting changelog_generator.py.

### Pdf_Converter.py
* This script converts files between different formats.
    It is currently hardcoded to convert .docx to .pdf.

### PlotRGB.py
* This script prompts the user for the path to a folder containing Landsat 5 bands and the function plots a natural color image of the satellite image and prints some basic information about the data.

### random_caps.py
* This script takes a text file of ASCII characters, randomly capitalizes them, and writes them out to a new text file.

### README.md
* This readme file.

### sentiment_analysis.py
* This script conducts sentiment analysis, assessing subjectivity and polarity of text data stored in a .csv file.

### simplified_roulette.py
* This script simulates a simplified (only color bets and straight bets) version of roulette with three different roulette wheels (No Zero, French/Single Zero, and American/Double Zero). 

### slot_machine.py
* This script simulates how upper confidence bound reinforcement learning works with a slot machine and prompts the user for the beginning balance and how many times to play.

### spreadsheet_cleaner.py
* This script removes leading, trailing, and double whitespace from Excel spreadsheets.

### text.txt
* A test file for random_caps.py.

### twoSum.py
* Finds the index of two values in a list that adds up to the target number

### webscraper.py
* This script takes the url for the WM CS website and extracts info about the department and courses offered.
