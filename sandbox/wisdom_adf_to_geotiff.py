import gdal

# run with
# exec(open("C:/Users/David/Documents/College/DATA_440_Spatial/spatial-data-discovery.github.io/sandbox/wisdom_adf_to_ascii.py").read())
# in qgis console

FILEPATH = "C:/Users/David/Desktop/af_acc_30s_grid/af_acc_30s/af_acc_30s/w001001.adf"
OUTPUT_PATH = "C:/Users/David/Desktop/conversion_output.tiff"

# Won't convert to anything except GTiff (GeoTiff)
print('converting...')
gdal.Warp(OUTPUT_PATH, FILEPATH, format='GTiff')
print('done')



