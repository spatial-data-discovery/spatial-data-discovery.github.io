#!/usr/bin/env python3
#
# nc_write.py
#
# LAST EDIT: 2019-10-28
#
# This script writes an NetCDF file.

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
    my_dir = os.path.expanduser("~")

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
    f.createDimension('y', 1000)
    y = f.createVariable('y', 'i', ('y',) )
    y[:] = numpy.arange(0, 1000, 1, int)
    y.units = 'pixels'

    # Create x dimension & variable:
    f.createDimension('x', 1000)
    x = f.createVariable('x', 'i', ('x',))
    x[:] = numpy.arange(0, 1000, 1, int)
    x.units = 'pixels'

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
    img[0] = numpy.random.randint(255, size=(1000,1000))
    img[1] = numpy.random.randint(255, size=(1000,1000))
    img[2] = numpy.random.randint(255, size=(1000,1000))

f.close()
