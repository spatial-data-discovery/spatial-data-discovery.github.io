import gdal
import os

# FILEPATH = input("Enter the path to the NetCDF file: ")
FILEPATH = "C:/Users/David/Documents/College/DATA_440_Spatial/netcdf_conv_assignment/conv2_part2_wisdom.nc"

# Open the NetCDF file
# net_file = gdal.Open(FILEPATH, gdal.GA_ReadOnly)
net_file = gdal.Open("NETCDF:" + FILEPATH + ":image")

# Get the metadata
print('Metadata')
meta_data = net_file.GetMetadata_Dict()
for key in meta_data.keys():
    print(f"{key} {meta_data[key]}")
print()

# Write the output file
in_filename = os.path.basename(FILEPATH)
in_dirname = os.path.dirname(FILEPATH)
out_filename = os.path.splitext(in_filename)[0] + '_EVI.tiff'
out_filepath = os.path.join(in_dirname, out_filename)
gdal.Warp(out_filepath, net_file, dstSRS='EPSG:4326')

# Add it to QGIS
iface.addRasterLayer(out_filepath, out_filename)




