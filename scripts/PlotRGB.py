# PlotRGB.py
#
# Author: Heather Baier
#
# Date: 2020-02-09
#
# This script prompts the user for the path to a folder contiang 
# Landsat 5 bands and the function plots a natural color image of the
# satellite image and prints some basic infomration about the data
#
# Required Modules
import matplotlib.pyplot as plt
import rasterio as rio
import numpy as np
import os

def ReadRaster(band, files, folder):
    """
        Reads in a raster band within a folder

        Inputs:
            - band: The band number to read in 
            - files: A list of landsat bands in a folder
            - folder: Path to a folder containing the desired band
        
        Outputs:
            - Raster object of desired band

    """
    band = [b for b in files if band in b]
    rast = rio.open(folder + band[0])
    rast = rast.read(1)
    return rast

def grabMTL(mtlFile, val):
    """
        Opens and MTL (metadata) file and return the desired value

        Inputs:
            - mtlFile: Path to an MTL file
            - val: The desired value (ex. 'WRS_PATH')
        
        Outputs:
            - The desired value as a float
    """
    mtl = open(mtlFile).read()
    mtl = mtl.splitlines()
    mtl = [v for v in mtl if val in v]
    mtl = float(mtl[0].split("=")[1])
    return mtl

def PlotRGB(folder):
    """
        The users inputs the path to a folder containing Landsat 5 bands 
        and the function plots and RGB image of the satellite image.
        
        Inputs:
            - folder: Path to folder containg Landsat 5 bnads (ex. './LT05_L1GS_117049_20090928_20161025_01_T2/')
        
        Outputs:
            - Natural color satellite image

        Prints:
            - Path, Row of image
            - Percent of image covered in clouds
            - Percent of land in image covered in clouds
    """
    files = os.listdir(folder)
    matching = [mtl for mtl in files if "_MTL.txt" in mtl]
    mtlPath = folder + matching[0]
    
    # Read in the specified satellite band
    band1 = ReadRaster("_B3.TIF", files, folder)
    band2 = ReadRaster("_B4.TIF", files, folder)
    band3 = ReadRaster("_B5.TIF", files, folder)

    # Stack the bands into a numpy array
    rgb = np.dstack((band3, band2, band1))

    # Plot the natural color image
    plt.imshow(rgb)
    
    # Get the basic data from the MTL file
    path = grabMTL(mtlPath, "WRS_PATH")
    row = grabMTL(mtlPath, "WRS_ROW")
    cc = grabMTL(mtlPath, "CLOUD_COVER")
    ccl = grabMTL(mtlPath, "CLOUD_COVER_LAND")

    # Print the basic information
    print("\nThe image covers (path, row): (", str(path), ",", str(row) + ")")
    print(str(cc) + "% of the image is covered in cloud.")
    print(str(ccl) + "% of the land in the image is covered in cloud.")
    
    return rgb
	    

if __name__ == '__main__':
    folder = str(input("Enter path to folder holding Landsat bands: "))
    PlotRGB(folder)
