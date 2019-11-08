# You may run this file from a Python command line using:
# `exec(open("/Users/Liz/Documents/DATA440/hdf_qgis_rosen.py").read())`

#For Friday, see if you can convert the .ADF file (link available in FAQ discussion board) to an .ASC file in Python. If not using gdal, let the user choose the file (command line argument or input prompt).

# https://gis.stackexchange.com/questions/77917/converting-gtiff-to-ascii-grid-using-qgis-gdal-translate
# https://viewer.nationalmap.gov/tools/rasterconversion/Convert_ArcGrid_to_XYZ_with_GDAL.html
import glob
import os
import os.path

import gdal

#work_dir = "/Users/Liz/Documents/DATA440"
work_dir = "/Users/Liz/Documents/DATA440/af_acc_15s"
my_adf = "w001001.adf"
# try passing the adf directory
#my_adf = "af_acc_15s"
my_asc = "test.asc"
my_asc = os.path.join(work_dir, my_asc)

file_path = os.path.join(work_dir, my_adf)
#check if the file exists
if os.path.isdir(file_path):
    print("found the directory")
else:
    raise IOError("No file found")

#gdal_translate -of AAIGrid lu_krs_attr.tif test_grid.asc
gdal_translate -of AAIGrid my_adf my_asc

''' fails because
File "<string>", line 30
    gdal_translate -of AAIGrid my_adf my_asc
                             ^
SyntaxError: invalid syntax '''
