import glob
import os
import os.path

import gdal

path = r'C:\Users\giraf\OneDrive\Documents\spatial_data\conv2_raster\fire\all_fires' # use your path
all_files = glob.glob(path + "/*.nc")
print(len(all_files))

cdf_layer = gdal.Open(all_files[0], gdal.GA_ReadOnly)
str_file_name = str(cdf_layer)

out_file = os.path.splitext(str_file_name)[0] + 'to.tiff'
out_path = r'C:\Users\giraf\OneDrive\Documents\spatial_data\conv2_raster\fire\all_fires\output.tiff'

gdal.Warp(out_path, cdf_layer)

iface.addRasterLayer(out_path, out_file)
