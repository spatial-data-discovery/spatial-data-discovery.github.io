'''
Averaging climate and weather data (netCDF) by time
@Author Ian Thompson
'''
import xarray as xr
import netCDF4 as nd
from netCDF4 import Dataset, num2date
import pandas as pd
import sys
#import argv
if sys.argv[1] == '--help' or '-h':
    print('Place a netCDF file in the folder of this script, run the script with the command\n'
          'python netcdf_mean.py YourFile.nc\n\n'
          'Your output file will be\n'
          'mean_YourFile.nc')
else:
    file = './' + str(sys.argv[1])
    tp = nd.Dataset(file, 'r', Formate='netCDF4')
    var_list = []

    for var in tp.variables:
        print("Name: ", var,
           "|| Units: ", tp[var].units,
           "|| Shape: ", tp[var].shape,
           "|| Long Name: ", tp[var].long_name)
        var_list.append(var)

    tp_xr = xr.open_dataset('./tp_18_19.nc')
    tp_mean = tp_xr.resample(time='1M').mean()

    for var in tp_mean.variables:
        print("Name: ", var,
                  "|| Units: ", tp[var].units,
                  "|| Shape: ", tp[var].shape,
                  "|| Long Name: ", tp[var].long_name)

    output = './' + 'mean_' + sys.argv[1]

    tp_mean.to_netcdf(output)

    print('##################################################')

    #
    # ###https://stackoverflow.com/questions/45796170/calculating-monthly-mean-from-daily-netcdf-file-in-python
    # ###https: // stackoverflow.com / questions / 28420988 / how - to - read - netcdf - file - and -write - to - csv - using - python
