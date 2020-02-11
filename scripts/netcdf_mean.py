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

def main(nc_file):

    file = './' + str(nc_file)
    print(file)
    tp = nd.Dataset(file, 'r', Formate='netCDF4')

    for var in tp.variables:
        print("Name: ", var,
              "|| Units: ", tp[var].units,
              "|| Shape: ", tp[var].shape,
              "|| Long Name: ", tp[var].long_name)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Averages the a netCDF file across time, writes out to new file")
    p.add_argument('file', nargs='?', help="The file path")
    args = p.parse_args()

    main(args.file)