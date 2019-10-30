#!/usr/bin/env python3
#
# hdf_qgis.py
#
# VERSION 0.1
# LAST EDIT: 2019-10-28
#
# Use this script to read an NETcdf spatial data file,
# convert the NETcdf dataset to a GeoTIFF, and
# visualize the GeoTIFF in QGIS
#
# This script assumes that your NETcdf file is located
# in a directory defined by an environment variable "DS_WORKSPACE"
# or else is in your home directory
#
# You may run this file from a Python command line using:
# `exec(open("nc_TogeoTiff_oforiaddae.py").read())`
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
# Set up directories and file names:
try:
    work_dir = os.environ['DS_WORKSPACE']
except:
    work_dir = os.path.expanduser("~")

file_paths = glob.glob(os.path.join(work_dir, "*.nc"))
modis_path = ""
modis_file = ""
if len(file_paths) > 0:
    modis_path = file_paths[0]
    modis_file = os.path.basename(modis_path)
else:
    raise IOError("No file found!")

# Open ncs file
nc_data = gdal.Open(modis_path, gdal.GA_ReadOnly)


# Create an output GeoTIFF raster
out_file = os.path.splitext(modis_file)[0] + '_nc.tiff'
out_path = os.path.join(work_dir, out_file)
gdal.GetDriverByName("GTiff").CreateCopy(out_path, nc_data, 0)

# Add GeoTIFF to your map
iface.addRasterLayer(out_path, out_file)
