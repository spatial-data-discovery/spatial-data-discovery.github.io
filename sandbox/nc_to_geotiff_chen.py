import os
import os.path

import gdal

#NOTE: you have to code the direcory and filename
work_dir = "/Users/jiaying/Downloads/DATA440/conv_scripts/population" #directory of the file
my_file = "conv2_part2_chen.nc" #filename

file_path = os.path.join(work_dir, my_file)
#check if the file exists
if os.path.isfile(file_path):
    nc_file = os.path.basename(file_path)
else:
    raise IOError("No file found! \
    Note that the file path is hard coded \
    and you have to change it manually in this script.")

src_ds = gdal.Open(file_path, gdal.GA_ReadOnly)

#Open output format driver, see gdal_translate --formats for list
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
iface.addRasterLayer(out_path, out_file)
