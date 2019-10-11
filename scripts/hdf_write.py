#!/usr/bin/env python3
#
# hdf_write.py
#
# VERSION 0.2
#
# LAST EDIT: 2019-10-11
#
# This script writes an HDF5 file.

###############################################################################
# IMPORT MODULES
###############################################################################
import os
import os.path
import sys

import h5py
import numpy

###############################################################################
# FUNCTIONS
###############################################################################
def set_attr(hf, attr_name, attr_val, obj_path):
        """
        Name:     set_attr
        Inputs:   - h5py File (hf)
                  - str, attribute name (attr_name)
                  - [dtype], attribute value (attr_val)
                  - str, path to group/dataset object (obj_path)
        Outputs:  None.
        Features: Sets given attribute to given path;
                  * raises exception upon failure
        """
        try:
            # Typecast strings to data:
            if isinstance(attr_val, str):
                attr_val = attr_val.encode('utf-8')
            elif attr_val is None:
                attr_val = "".encode('utf-8')

            hf[obj_path].attrs.create(name=attr_name, data=attr_val)
        except:
            err_msg = "could not set '%s' to '%s' at '%s'" % (
                attr_val, attr_name, obj_path)
            print(err_msg)
            raise


###############################################################################
# MAIN
###############################################################################
# Check Python major/minor version (e.g., 3.7) for f string support:
f_str = True
py_maj, py_min = sys.version_info[:2]
if py_maj == 3 and py_min < 6:
    f_str = False

# Create a system varianble called "DS_WORKSPACE" and save working path to it
try:
    my_dir = os.environ['DS_WORKSPACE']
except:
    my_dir = os.path.expanduser("~")

my_file = "test.hdf"
hdf_path = os.path.join(my_dir, my_file)

if os.path.isfile(hdf_path):
    # Open for appending
    print('opening file')
    hdfile = h5py.File(hdf_path, 'r+')
else:
    # Create new file
    print('creating file')
    hdfile = h5py.File(hdf_path, 'w')

# Writing root attributes
if False:
    set_attr(hdfile, "author", "Tyler W. Davis", "/")
    set_attr(hdfile, "date", "2019-10-04", "/")
    set_attr(hdfile, "affiliation", "William & Mary", "/")

# Create a group
if False:
    if "/store" in hdfile:
        print("/store group already exists!")
    else:
        print("Creating group")
        hdfile.create_group("/store")
        set_attr(hdfile, "name", "storage container", "/store")

# Create an example dataset in its own group
if False:
    if "/data/raster" in hdfile:
        print("/data/raster already exists")
    else:
        print("Creating dataset /data/raster")
        my_data = numpy.random.randint(255, size=(360, 720))
        hdfile.create_dataset("/data/raster", data=my_data, chunks=(90, 90))
        set_attr(hdfile, "name", "data directory", "/data")
        set_attr(hdfile, "file_type", "raster", "/data/raster")

# Create the assignment dataset:
if False:
    my_data_file = "assignment.asc"
    my_proj_file = "assignment.prj"
    my_data_path = os.path.join(my_dir, my_data_file)
    my_proj_path = os.path.join(my_dir, my_proj_file)
    print(os.path.isfile(my_data_path))
    print(os.path.isfile(my_proj_path))

    # Read data:
    rdat = numpy.array([], dtype="float")
    head = []
    nrows = 0
    ncols = 0
    with open(my_data_path) as f:
        head = [next(f) for x in range(6)]
        for line in f:
            nrows += 1
            tmp = line.strip().split()
            vals = [float(x) for x in tmp]

            # Check number of columns, print anytime value changes:
            ncols_temp = len(vals)
            if ncols != ncols_temp:
                if f_str:
                    print(f"Found new ncol {ncols_temp} at row {nrows}")
                else:
                    print("Found new ncol %d at row %d" % (ncols_temp, nrows))
            ncols = ncols_temp

            # Save data to array:
            rdat = numpy.append(rdat, vals)

    if f_str:
        print(f"Read {nrows} rows and {ncols} columns")
    else:
        print("Read %d rows and %d columns" % (nrows, ncols))

    # Resize to 2D array:
    rdat.resize((nrows, ncols))
    print("Data size: (%d, %d)" % rdat.shape)

    # Configure header:
    head_dict = {}
    for line in head:
        words = line.strip().split()
        head_dict[words[0]] = words[1]

    # Read projection information:
    with open(my_proj_path) as f:
        line = f.readline()
        head_dict['crs'] = line

    # Save data to HDF5 file:
    dset = "/data/assignment"
    if dset in hdfile:
        if f_str:
            print(f"{dset} already exists")
        else:
            print("%s already exists" % (dset))
    else:
        print("Creating dataset", dset)
        try:
            hdfile.create_dataset(name=dset,
                                  data=rdat.astype(int),
                                  chunks=True)
        except TypeError as e:
            print(e)
        else:
            for key in head_dict:
                val = head_dict[key]
                set_attr(hdfile, key, val, dset)

hdfile.close()
