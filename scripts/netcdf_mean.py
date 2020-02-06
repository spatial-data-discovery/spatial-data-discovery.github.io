'''
Averaging climate and weather data (netCDF) by time
@Author Ian Thompson
'''
import xarray as xr
import netCDF4 as nd
from netCDF4 import Dataset, num2date
import sys
#import argv

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
tp_mean = tp_xr.resample(time='m').mean()

output = './' + 'mean_' + sys.argv[1]

tp_mean.to_netcdf(output)

###https://stackoverflow.com/questions/45796170/calculating-monthly-mean-from-daily-netcdf-file-in-python
