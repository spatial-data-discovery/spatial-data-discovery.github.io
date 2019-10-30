#!/usr/bin/env python3
#
# hdf_qgis.py
#
# VERSION 0.1
# LAST EDIT: 2019-10-28
#
# Use this script to read an HDF4 spatial data file,
# convert the HDF dataset to a GeoTIFF, and
# visualize the GeoTIFF in QGIS
#
# This script assumes you have downloaded a MODIS HDF4 dataset from
# LP DAAP data pool (https://lpdaac.usgs.gov/tools/data-pool/) or
# you have downloaded the example data provided by Saul Montoya from
# https://www.hatarilabs.com/s/HDFReproyectionPyQGIS.rar
#
# This script assumes that your hdf file is located
# in a directory defined by an environment variable "DS_WORKSPACE"
# or else is in your home directory
#
# You may run this file from a Python command line using:
# `exec(open("hdf_qgis.py").read())`
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

file_paths = glob.glob(os.path.join(work_dir, "*.hdf"))
modis_path = ""
modis_file = ""
if len(file_paths) > 0:
    modis_path = file_paths[0]
    modis_file = os.path.basename(modis_path)
else:
    raise IOError("No file found!")

# Open HDF file
hdf_layer = gdal.Open(modis_path, gdal.GA_ReadOnly)

if False:
    # Check out the datasets available. Note: each tuple has two strings:
    # the first is the subdataset name, the second a descriptor
    for my_layer in hdf_layer.GetSubDatasets():
        print(my_layer)

# Find the layer you want to open (index 1 has EVI)
rlayer = gdal.Open(hdf_layer.GetSubDatasets()[1][0], gdal.GA_ReadOnly)

if False:
    # Let's take a look at the metadata for this data layer
    for key in rlayer.GetMetadata_Dict():
        val = rlayer.GetMetadata_Dict()[key]
        print(key, val)

# Create an output GeoTIFF raster
out_file = os.path.splitext(modis_file)[0] + '_EVI.tiff'
out_path = os.path.join(work_dir, out_file)
gdal.Warp(out_path, rlayer, dstSRS='EPSG:4326')

# Add GeoTIFF to your map
iface.addRasterLayer(out_path, out_file)
