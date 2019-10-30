#!/usr/bin/env python3
#
# nc_qgis.py
#
# VERSION 0.1
# LAST EDIT: 2019-10-29
#
# Use this script to read an NetCDF spatial data file,
# convert the NC dataset to a GeoTIFF, and
# visualize the GeoTIFF in QGIS
#
#
###############################################################################
# IMPORT MODULES
###############################################################################
import glob
import os
import os.path

import gdal
###############################################################################
# MAIN
###############################################################################
work_dir = "/Users/MorganBrickey/Documents/FALL2019/SDD/netcdf_conversion"
my_file = "conv2_part2BRICKEY.nc"

file_path = os.path.join(work_dir, my_file)

#check if the file exists
if os.path.isfile(file_path):
    nc_file = os.path.basename(file_path)
else:
    raise IOError("No file found!")

# Open NC file
nc_layer = gdal.Open(modis_path, gdal.GA_ReadOnly)

# Create an output GeoTIFF raster
out_file = os.path.splitext(modis_file)[0] + '.tiff'
out_path = os.path.join(work_dir, out_file)
# gdal.Warp(out_path, rlayer, dstSRS='EPSG:4326') # spatial reference

# Add GeoTIFF to your map
iface.addRasterLayer(out_path, out_file)
