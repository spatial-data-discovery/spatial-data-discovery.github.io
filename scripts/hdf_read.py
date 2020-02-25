#!/usr/bin/env python3
#
# hdf_read.py
#
# VERSION 0.2
#
# LAST EDIT: 2020-02-25
#
# This script reads an HDF5 file.
#
###############################################################################
# IMPORT MODULES
###############################################################################
import os
import os.path

import h5py


###############################################################################
# MAIN
###############################################################################
def get_attr(hf, attr, group_path):
        """
        Name:     get_attr
        Features: Returns the given attribute for the given path
        Inputs:   - open h5py file object (hf)
                  - str, attribute name (attr)
                  - str, group path (group_path)
        Outputs:  str, attribute value (val)
        """
        if group_path in hf:
            if attr in hf[group_path].attrs.keys():
                try:
                    tmp = hf[group_path].attrs[attr]

                    if isinstance(tmp, str):
                        val = tmp
                    elif isinstance(tmp, numpy.ndarray):
                        val = tmp
                    else:
                        try:
                            val = tmp.decode('UTF-8')
                        except:
                            val = tmp
                except KeyError:
                    print("'%s' has no attribute '%s'" % (group_path, attr))
                    val = "UNDEFINED"
                except:
                    print(
                        ("attribute '%s' could not be retrieved "
                         "from path '%s'!") % (attr, group_path))
                    val = "UNDEFINED"
            else:
                print("'%s' has no attribute '%s'" % (group_path, attr))
                val = "UNDEFINED"
        else:
            print('path not defined!')
            val = "UNDEFINED"

        return val


def get_object_attrs(hf, obj_path):
        """
        Name:     get_object_attrs
        Features: Returns dictionary of group/dataset attributes
        Inputs:   - open h5py file object (hf)
                  - str, object path (obj_path)
        Outputs:  dict, session attributes (attrs_dict)
        """
        attr_dict = {}
        if obj_path is not None and obj_path in hf:
            for key in hf[obj_path].attrs.keys():
                val = hf[obj_path].attrs[key]
                if isinstance(val, bytes):
                    attr_dict[key] = val.decode('UTF-8')
                else:
                    attr_dict[key] = val
        else:
            print(
                "could not get attributes for %s; object does not exist!",
                obj_path)

        return attr_dict

def list_objects(hf, parent_path):
        """
        Name:     list_objects
        Features: Returns a sorted list of HDF5 objects under a given parent
        Inputs:   - open h5py file object (hf)
                  - str, HDF5 path to parent object
        Outputs:  list, HDF5 objects
        """
        rlist = []
        if parent_path in hf:
            try:
                hf[parent_path].keys()
            except:
                # Dataset has no members
                rlist = 0
            else:
                for obj in sorted(list(hf[parent_path].keys())):
                    rlist.append(obj)
        else:
            wmgs = "'%s' does not exist!" % (parent_path)
            print(wmgs)
            print('returning empty list')

        return rlist


def print_attrs(hf, group):
    """
    Name:     print_attrs
    Inputs:   - open h5py file object (hf)
              - str, path to group or dataset (group)
    Outputs:  None.
    Features: Prints the attributes for a given HDF5 group/dataset
    Depends:  get_object_attrs
    """
    if group in hf:
        d = get_object_attrs(hf, group)
        for key in d:
            val = d[key]
            print("%s: %s: %s" % (group, key, val))

###############################################################################
# MAIN
###############################################################################
# Set working directory to "DS_WORKSPACE" or default to local directory
try:
    my_dir = os.environ['DS_WORKSPACE']
except:
    my_dir = "."

my_file = "test.hdf"
hdf_path = os.path.join(my_dir, my_file)

# Reading root attributes
if os.path.isfile(hdf_path):
    hdfile = h5py.File(hdf_path, 'r')

    # Read objects (i.e., groups and datasets)
    my_objects = list_objects(hdfile, "/")
    my_groups = ["/"]
    for my_obj in my_objects:
        my_groups.append("/" + my_obj)

    for my_group in my_groups:
        print("Objects in", my_group)
        my_objects = list_objects(hdfile, my_group)
        if my_objects == 0:
            print("Found dataset")
        elif len(my_objects) == 0:
            print("> N/A")
        else:
            for my_obj in my_objects:
                print(">", my_obj)

    # Read attributes
    print("Attributes:")
    for my_group in my_groups:
        print_attrs(hdfile, my_group)

    print_attrs(hdfile, "/data/raster")
    print_attrs(hdfile, "/data/assignment")

    hdfile.close()
