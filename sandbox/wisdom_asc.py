import os
import pandas as pd


def find_ascii(dirpath: str) -> list:
    """
    Find all the ASCII files in a directory

    :param dirpath:
    :return:
    """


def parse_header(filepath: str) -> dict:
    """
    Read the header info at the beginning of an ASCII
    file and return the number of rows, number of columns,
    and the "missing data" value

    :param filepath:
    :return:
    """


def parse_data(filepath: str, na_value: int) -> pd.DataFrame:
    """
    Read an ASCII file data into a DataFrame

    :param filepath:
    :return:
    """

def main(dirpath: str):
    """
    Takes a path to a directory and checks whether the ASCII raster
    files in that directory are internally consistent.

    :param filepath:  Path to a directory of ASCII raster files to check
    """


if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('filepath', help='Path to a directory containing ASCII raster files to check')

    args = p.parse_args()

    main(args.filepath)
