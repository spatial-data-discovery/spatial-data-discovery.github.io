'''
Averaging climate and weather data (netCDF) by time
@Author Ian Thompson
'''
import xarray as xr
import netCDF4 as nd
from netCDF4 import Dataset, num2date
import pandas as pd
import sys
import argparse
import warnings

def main(nc_file):
    file = './' + str(nc_file)
    print("File In: " + file)
    tp = nd.Dataset(file, 'r', Formate='netCDF4')

    for var in tp.variables:
        print("Name: ", var,
              "|| Units: ", tp[var].units,
              "|| Shape: ", tp[var].shape,
              "|| Long Name: ", tp[var].long_name)

    tp_xr = xr.open_dataset(file)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        tp_mean = tp_xr.resample(time='1M').mean()

    print(tp_mean.data_vars)
    print('##################################################')


    output = file + "_mean"

    print("File Out: " + output)

    tp_mean.to_netcdf(output)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Averages the a netCDF file across time, writes out to new file")
    p.add_argument('file', nargs='?', help="The file name - must be in the same folder as script")
    args = p.parse_args()

    main(args.file)

    ###https://stackoverflow.com/questions/45796170/calculating-monthly-mean-from-daily-netcdf-file-in-python
    ####https: // stackoverflow.com / questions / 28420988 / how - to - read - netcdf - file - and -write - to - csv - using - python
