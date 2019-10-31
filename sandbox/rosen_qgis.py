#!/usr/bin/env python3
#
# nc_qgis_rosen.py
#
# VERSION 0.1
# LAST EDIT: 2019-10-28
#
# You may run this file from a Python command line using:
# `exec(open("/Users/Liz/Documents/DATA440/hdf_qgis_rosen.py").read())`
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
work_dir = "/Users/Liz/Documents/DATA440/conv2"
my_file = "conv2_part2_ROSEN.nc"

file_path = os.path.join(work_dir, my_file)
#check if the file exists
if os.path.isfile(file_path):
    nc_file = os.path.basename(file_path)
else:
    raise IOError("No file found")

ds = gdal.Open("NETCDF:{0}:{1}".format(file_path, gdal.GA_ReadOnly)
#src_ds = gdal.Open(file_path, gdal.GA_ReadOnly)

#Open output format driver, see gdal_translate --formats for list
data=ds.ReadAsArray(0, 0, ds.RasterXSize, ds.RasterYSize)
data[data < 0] = 0

#https://riptutorial.com/gdal/example/25859/read-a-netcdf-file---nc--with-python-gdal
'''
format = "GTiff"
driver = gdal.GetDriverByName( format )

# Create an output GeoTIFF raster
out_file = os.path.splitext(nc_file)[0] + '.tiff'
out_path = os.path.join(work_dir, out_file)

#Output to new format
dst_ds = driver.CreateCopy( out_path, src_ds, 0 )

#Properly close the datasets to flush to disk
dst_ds = None
src_ds = None

# Add GeoTIFF to your map
iface.addRasterLayer(out_path, out_file)'''
