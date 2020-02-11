# README
--------
* LAST UPDATED: 2019-10-24
* ORGANIZATION: spatial-data-discovery
* REPOSITORY: spatial-data-discovery.github.io/scripts

## DESCRIPTION
This folder contains utility and general functionality scripts.

## Files

### Book_keeping.py
* This script takes in two excel files and compares them to update inventory.  

### caesar_cipher.py
* This script takes a message given by the user and encrypts it using a Caesar Cipher

### changelog_generator.py
* This script generates a changelog (Hopefully) to the professors specs programmatically.

### crosswind.py
* This script determines which runway pilots should use based on runways available, wind direction, and wind speed.

### darts.py
* This script is a throwing darts game that lets the user choose how many darts to throw at a circular dart board
  and tell them what percent of the darts landed on the board.

### embassy_news_scraper.py
* This script takes a url of a news source from one of Chinese embassy websites and extracts its description.

### hdf_qgis.py
* this script opens a MODIS HDF4 file using GDAL, converts it to a GeoTIFF, and opens it for visualization in QGIS (tested using QGIS 3.4)

### hdf_read.py
* this script opens and reads an HDF5 file using h5py

### hdf_write.py
* this script creates a new and edits an existing HDF5 file using h5py

### josephus.py
* This script demonstrates the way linked lists work as well as adding a fun game to the mix!
  Josephus takes any number inputted by the user and makes a linked list of 1 to that number.
  It will then rotate the linked list so the first value becomes the last and then removes the
  new first value. It will continue to do this until there is only one number left.
  This is the survivor!

### keywords.py
* This script takes a text file, get the most commonly used words, and then googles for links related to these words

### magic8ball.py
* This script asks the user a question and then gives them the response a Magic 8 ball would

### movie_script_scraper.py
* This code scrapes movie scripts from Scripts.com and saves the text in a .txt file

### music_randomizer.py
* This script randomizes and organizes MP3 files in a folder or on a USB drive

### nc_read.py
* this script reads attributes, variables, and dimensions from a NetCDF "classic" data file using scipy.io

### nc_write.py
* this script creates a NetCDF "classic" data file and writes attributes, variables, and dimensions to the file using scipy.io

### Pdf_Converter.py
* This script converts files between different formats. It is currently hardcoded to convert .docx to .pdf.

### PlotRGB.py
* This script prompts the user for the path to a folder containing Landsat 5 bands and the function plots a natural color image of the    satellite image and prints some basic infomration about the data

### random_caps.py
* This script takes a text file of ASCII characters, randomly capitalizes them,
  and writes them out to a new text file

### README.md
* this readme file

### slot_machine.py
* This script simulates how upper confidence bound reinforcement learning works with a slot machine and prompts the user for the beginning balance and how many times to play

### spreadsheet_cleaner.py
* This script removes leading, trailing, and double whitespace from Excel spreadsheets

### text.txt
* a test file for random_caps.py

### twoSum.py
* Finds the index of two values in a list that adds up to the target number

### webscraper.py
* This script takes the url for the WM CS website and extracts info about the department and courses offered.
