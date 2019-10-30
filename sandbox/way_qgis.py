import glob
import os
import os.path

import gdal

path = r'C:\Users\giraf\OneDrive\Documents\spatial_data\conv2_raster\fire\all_fires' # use your path

out_path = r'C:\Users\giraf\OneDrive\Documents\spatial_data\conv2_raster\fire\all_fires\output.tiff'

cdf_layer = gdal.Open('conv_part2_way.nc', gdal.GA_ReadOnly)
print(cdf_layer)

#rlayer = gdal.Open(cdf_layer.GetSubDatasets()[0][0], gdal.GA_ReadOnly)

#dal.Warp(out_path, rlayer, dstSRS='EPSG:4326')
#iface.addRasterLayer(out_path, out_file)
