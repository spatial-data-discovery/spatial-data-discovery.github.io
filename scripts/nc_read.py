#!/usr/bin/env python3
#
# nc_write.py
#
# LAST EDIT: 2020-03-24
#
# This script writes an NetCDF file.

###############################################################################
# IMPORT MODULES
###############################################################################
import os
import os.path

import numpy
from scipy.io import netcdf

###############################################################################
# FUNCTIONS
###############################################################################
def print_keys(my_obj):
    """
    Name:     print_keys
    Inputs:   dict, dictionary (my_obj)
    Outputs:  None
    Features: Prints key-value pairs for an ordered dictionary
    """
    try:
        for key in my_obj.keys():
            value = my_obj[key]
            if isinstance(value, bytes):
                value = value.decode("utf-8")

            print("  %s: %s" % (key, value))
    except AttributeError as e:
        print("Object has no keys.", e)


###############################################################################
# MAIN
###############################################################################
try:
    my_dir = os.environ['DS_WORKSPACE']
except:
    my_dir = "."

my_file = "test.nc"
nc_path = os.path.join(my_dir, my_file)

# Open a new NetCDF file
if os.path.isfile(nc_path):
    f = netcdf.netcdf_file(nc_path, 'r')

    # Print file attributes:
    print("File attributes for %s" % (f.filename))
    print_keys(f._attributes)

    print("File dimensions")
    print_keys(f.dimensions)

    print("File variables")
    print_keys(f.variables)

    # Print variable attributes:
    for key in f.variables.keys():
        print(key)
        print_keys(f.variables[key]._attributes)

    # Read data
    if 'image' in f.variables:
        # Copy data out of file avoids error when closing the file.
        my_data = f.variables['image'].data.copy()
        print("Read %d bands, %d rows, %d cols" % my_data.shape)

    f.close()
