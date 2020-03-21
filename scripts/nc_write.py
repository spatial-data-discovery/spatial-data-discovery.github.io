#!/usr/bin/env python3
#
# nc_write.py
#
# LAST EDIT: 2020-03-21
#
# This script writes an NetCDF file.
# Usage: run this script in tandem with nc_read.py.
# Each time, change the next False statement to True.

###############################################################################
# IMPORT MODULES
###############################################################################
import os
import os.path

import datetime
import numpy
from scipy.io import netcdf


##############################################################################
# GLOBAL VARIABLES:
##############################################################################
ERROR_VAL = -9999


###############################################################################
# FUNCTIONS
###############################################################################
def nc_history():
    """
    Name:     nc_history
    Input:    None.
    Output:   string (my_str)
    Features: Returns a string for netCDF file history field based on the file's
              creation date
    """
    my_str = "created %s" % datetime.date.today()
    return my_str



###############################################################################
# MAIN
###############################################################################
# Create a system varianble called "DS_WORKSPACE" and save working path to it
try:
    my_dir = os.environ['DS_WORKSPACE']
except:
    my_dir = "."

my_file = "test.nc"
nc_path = os.path.join(my_dir, my_file)

# Create a new NetCDF file
f = netcdf.netcdf_file(nc_path, 'w')

if True:
    # Write file attributes:
    f.history = nc_history()
    f.contact = 'Tyler W. Davis (twdavis@wm.edu)'
    f.title = 'Example data created for Spatial Data Discovery'
    f.note = 'You may safely delete this file'
    f.institution = 'William & Mary'

if False:

    # Create y dimension and a variable
    # name the variable 'y' of type 'i'nteger of dimension ('y',)
    f.createDimension('y', 720)
    y = f.createVariable('y', 'i', ('y',) )
    y[:] = numpy.arange(0, 720, 1, int)
    y.units = 'row index'

    # Create x dimension & variable:
    f.createDimension('x', 960)
    x = f.createVariable('x', 'i', ('x',))
    x[:] = numpy.arange(0, 960, 1, int)
    x.units = 'col index'

    # Create color dimension & variable
    f.createDimension('color', 3)
    color = f.createVariable('color', 'i', ('color',))
    color.standard_name = 'RGB'
    color.units = 'red green blue color bands'

if False:

    # Create random color image variable:
    img = f.createVariable('image', 'i', ('color','y','x'))
    img._FillValue = ERROR_VAL
    img.missing_value = ERROR_VAL
    img.long_name = 'Random RGB color band image'
    img.units = 'none'
    img.valid_range = numpy.array([0, 255])
    img[0] = numpy.random.randint(255, size=(720,960))
    img[1] = numpy.random.randint(255, size=(720,960))
    img[2] = numpy.random.randint(255, size=(720,960))

    # Reference for Attribute convensions
    # http://www.bic.mni.mcgill.ca/users/sean/Docs/netcdf/guide.txn_18.html
    # David Fulker, Unidata Program Center Director, UCAR

f.close()
