#!/usr/bin/env python3
#
# vector.py
#
# VERSION 0.1
#
# LAST EDIT: 2019-09-15
#
# This script reads coordinates from images' Exif tags, and creates an XY point
# file for plotting their location in QGIS.
#
##############################################################################
# REQUIRED MODULES
##############################################################################
import glob
import os.path

import exifread

###############################################################################
# PARAMETER DEFINITIONS:
###############################################################################
# Currently support image types:
img_types = (".jpg", ".JPG", ".jpeg")

##############################################################################
# FUNCTIONS
##############################################################################
def find_image_files(my_dir):
    """
    Name:     find_image_files
    Inputs:   str, directory name (my_dir)
    Outputs:  list, image paths
    Features: Searches a single directory for image files
    Depends:  img_types (global variable)
    """
    my_files = []
    for img_type in img_types:
        s_str = os.path.join(my_dir, "*%s" % (img_type))
        my_files += glob.glob(s_str)
    my_files = sorted(list(set(my_files)))

    return my_files


def _convert_to_degress(value):
    """
    Name:     _convert_to_degress
    Inputs:   exifread.utils.Ratio (value)
    Outputs:  float
    Features: Helper function to convert the GPS coordinates stored in the EXIF
              to degress in float format
    Ref:      https://gist.github.com/snakeye/fdc372dbf11370fe29eb
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


def getGPS(filepath):
    '''
    Name:     getGPS
    Inputs:   str (filepath)
    Outpus:   dict
    Features: Returns gps data if present other wise returns empty dictionary
    Note:     file must be opened as binary ('rb')
    Ref:      https://gist.github.com/snakeye/fdc372dbf11370fe29eb
    '''
    with open(filepath, 'rb') as f:
        tags = exifread.process_file(f)
        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')
        if latitude:
            lat_value = _convert_to_degress(latitude)
            if latitude_ref.values != 'N':
                lat_value = -lat_value
        else:
            return {}
        if longitude:
            lon_value = _convert_to_degress(longitude)
            if longitude_ref.values != 'E':
                lon_value = -lon_value
        else:
            return {}
        return {'latitude': lat_value, 'longitude': lon_value}
    return {}


def process_img_files(file_dir, out_file):
    """
    Name:     process_img_files
    Inputs:   - str, file directory (file_dir)
              - str, output file name (out_file)
    Ouputs:   None
    Features: Processes the coordinates from image files located in the given
              directory and writes them to file
    Depends:  - find_image_files
              - getGPS
              - writeline
              - writeout
    """
    header = "ID,LAT,LON,NAME\n"
    output_path = os.path.join(file_dir, out_file)
    if os.path.isfile(output_path):
        print("WARNING: overwriting file %s" % out_file)
    writeout(output_path, header)

    if os.path.isdir(file_dir):
        my_files = find_image_files(file_dir)
        num_files = len(my_files)
        if num_files > 0:
            for i in range(num_files):
                my_file = my_files[i]
                f_name = os.path.basename(my_file)
                f_gps = getGPS(my_file)
                try:
                    f_lat = f_gps['latitude']
                    f_lon = f_gps['longitude']
                except:
                    print('No GPS information for file %s' % my_file)
                else:
                    my_line = "%d,%f,%f,%s\n" % (i, f_lat, f_lon, f_name)
                    writeline(output_path, my_line)
        else:
            print("No image files found!")
    else:
        print("Directory not found!")


def writeline(f, d):
    """
    Name:     writeout
    Input:    - str, file name with path (f)
              - str, data to be written to file (d)
    Output:   None
    Features: Appends an existing file with data string
    """
    try:
        with open(f, 'a') as my_file:
            my_file.write(d)
    except:
        raise IOError("Can not write to output file.")

def writeout(f, d):
    """
    Name:     writeout
    Input:    - str, file name with path (f)
              - str, data to be written to file (d)
    Output:   None
    Features: Writes new/overwrites existing file with data string
    """
    try:
        with open(f, 'w') as my_file:
            my_file.write(d)
    except:
        raise IOError("Can not write to output file.")


##############################################################################
# MAIN
##############################################################################
if __name__ == "__main__":
    my_dir = input('Enter the path to image folder: ')
    my_outfile = "points.txt"
    process_img_files(my_dir, my_outfile)

if None:
    out_file = os.path.join(my_dir, my_outfile)

    # For QGIS 2.18.17 (on Mac/Linux)
    uri = "file://%s?encoding=%s&delimiter=%s&xField=%s&yField=%s&crs=%s" % (out_file, "UTF-8",",", "LON", "LAT","epsg:4326")
    csv_layer=QgsVectorLayer(uri,"points","delimitedtext")
    QgsMapLayerRegistry.instance().addMapLayer(csv_layer)

    # For QGIS 3.14 (on Windows)
    out_file = out_file.replace("\\", "/")
    uri = "file:///%s?encoding=%s&delimiter=%s&xField=%s&yField=%s&crs=%s" % (out_file, "UTF-8",",", "LON", "LAT","epsg:4326")
    csv_layer=QgsVectorLayer(uri,"points","delimitedtext")
    QgsProject.instance().addMapLayer(layer)
