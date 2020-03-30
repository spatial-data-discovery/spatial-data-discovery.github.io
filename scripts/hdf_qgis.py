#!/usr/bin/env python3
#
# hdf_qgis.py
#
# VERSION 0.2
# LAST EDIT: 2020-03-30
#
# Use this script to read an HDF4 spatial data file,
# convert the HDF dataset to a GeoTIFF, and
# visualize the GeoTIFF in QGIS
#
# Let's say you want to extract a single data layer from an HDF file
# that has lots of datasets. One format that is easy to work with in a GIS
# is the GeoTIFF or georeferenced tagged image file format. GeoTIFF is not
# for every data type; see URL below for some strengths/weaknesses.
# https://earthdata.nasa.gov/esdis/eso/standards-and-references/geotiff
#
# This script assumes you have downloaded a MODIS HDF4 dataset from
# LP DAAP data pool (https://lpdaac.usgs.gov/tools/data-pool/) or
# you have downloaded the example data provided by Saul Montoya from
# https://www.hatarilabs.com/s/HDFReproyectionPyQGIS.rar
#
# This script assumes that your hdf file is located
# in a directory defined by an environment variable "DS_WORKSPACE"
# or else is in the local directory.
#
# You may run this file from a Python command line using:
# `exec(open("hdf_qgis.py").read())`
#
# NOTE: for running on the commandline in Windows, I used the
# OSGeo4W Shell, which provides links to the necessary libraries
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
    work_dir = "."

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

# Let's take a look at its metadata:
for key in hdf_layer.GetMetadata_Dict():
    val = hdf_layer.GetMetadata_Dict()[key]
    print(key, val)

# Check out the datasets available. Note: each tuple has two strings:
# the first is the subdataset name, the second a descriptor
for my_layer in hdf_layer.GetSubDatasets():
    print(my_layer)

# Find the layer you want to open (index 1 has EVI)
rlayer = gdal.Open(hdf_layer.GetSubDatasets()[1][0], gdal.GA_ReadOnly)

# See what's all available with this class:
dir(rlayer)

# Let's take a look at the metadata for this data layer
for key in rlayer.GetMetadata_Dict():
    val = rlayer.GetMetadata_Dict()[key]
    print(key, val)

# Create an output GeoTIFF raster
# NOTE: although the data layer says it is in EPSG:9122; it's unknown
# so, let's create a GeoTIFF in the standard EPSG:4326 (WGS84)
out_file = os.path.splitext(modis_file)[0] + '_EVI.tiff'
out_path = os.path.join(work_dir, out_file)
gdal.Warp(out_path, rlayer, dstSRS='EPSG:4326')

# Add GeoTIFF to your map (only run if you are in QGIS Python console)
try:
    iface.addRasterLayer(out_path, out_file)
except NameError:
    exit()
