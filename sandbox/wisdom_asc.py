import glob
import os
import pandas as pd
import numpy as np


def is_ascii(filepath: str) -> bool:
    """
    Checks whether a file has 'NCOLS ' or 'NROWS ' at the beginning
    to determine whether it's an ASCII file

    :param filepath: Path to a file to check
    :return: Boolean indicating whether it's an ASCII raster file
    """
    f = open(filepath, 'r')
    try:
        first_line = f.readlines()[0].upper()
    except IndexError:  # If there's no first line it's probably not a text file
        return False
    f.close()
    # If it starts with the correct words, it's what we're looking for
    if first_line.startswith('NROWS ') or first_line.startswith('NCOLS '):
        return True

    return False


def find_ascii(dirpath: str) -> list:
    """
    Find all the .asc and .txt files in a directory.

    :param dirpath: Path to a directory to find .asc and .txt files in
    :return: List of the .asc and .txt files in that directory
    """
    asc_files = glob.glob(dirpath + "/*.asc")

    # Check the text files to find ones that look like ASCI raster files
    possible_files = glob.glob(dirpath + '/*.txt')
    for pos in possible_files:
        if is_ascii(pos):
            asc_files.append(pos)

    return asc_files


def find_all(dirpath: str) -> list:
    """
    Returns all the ASCII raster files in a directory and in all its sub-directories.
    This function has the potential to take forever but it doesn't rely on
    file extensions to find the files

    :param dirpath: Path to a directory to check for ASCII raster files
    :return: A list of every ASCII raster file
    """
    possible_files = []
    # Go though everything
    for root, directory, files in os.walk(dirpath):
        for _file in files:
            # If it's what we're looking for, put it in the list
            if is_ascii(_file):
                possible_files.append(os.path.abspath(_file))

    return possible_files


def parse_file(filepath: str) -> tuple:
    """
    Read the header info at the beginning of an ASCII
    file and put it into a dictionary for later use

    Also read the data into a DataFrame so that we can check
    it against the values in the dictionary

    :param filepath: Path to an ASCII raster file
    :return: A dictionary of the header information, A DataFrame of the data
    """
    f = open(filepath, 'r')
    contents = f.readlines()
    f.close()
    # Look at the first 6 lines to get the header
    # This doesn't work at all because the header doesn't have
    # to be six lines
    header = {}
    try:
        for i in range(6):
            line = contents[i].split(' ')  # Split on the space
            name = line[0].strip().upper()  # Get the name of the field
            value = line[-1].strip()  # Get the value of the field
            header[name] = value  # Add the header name and the value to the dictionary
    # Bad practice but here we are
    except:
        print(f'Error parsing the header for {os.path.basename(filepath)}')
        return None, None

    # Look at the rest to get the data into a DataFrame
    # Skip over the header data in the file
    try:
        data = pd.read_csv(filepath, delim_whitespace=True, header=None, skiprows=6)
    # Another bare except
    except:
        print(f'Error parsing data for {os.path.basename(filepath)}')
        return None, None

    return header, data


def is_consistent(header_info: dict, data: pd.DataFrame) -> bool:
    """
    Check the metadata values and see whether they match up with
    the DataFrame represenation of the data

    :param header_info: Dictionary of {field_name: field_value}
    :param data: DataFrame of the ASCII raster data
    :return: Boolean indicating whether everything matches up
    """
    if header_info is None or data is None:
        return False

    # If we were able to parse everything and build the
    # dictionary and DataFrame, check that everything
    # is consistent
    h_rows = int(header_info['NROWS'])
    h_cols = int(header_info['NCOLS'])

    d_rows = data.shape[0]
    d_cols = data.shape[1]

    # Check that the number of rows is the same
    if h_rows != d_rows:
        print(f'inconsistent number of rows. Header says {h_rows} but there are {d_rows} after line 6')
        return False
    # Check that the number of columns is the same
    if h_cols != d_cols:
        print(f'inconsistent number of columns. Header says {h_cols} but there are {d_cols}')
        return False

    # Check that every column is an integer or float column
    for col in data.columns:
        col_type = data[col].dtype
        # If the column isn't integers or floats, something is wrong
        # I don't know anything about NumPy's dtypes but this might break on
        # 32-bit architectures
        if not np.issubdtype(col_type, np.int64) and not np.issubdtype(col_type, np.float64):
            print(f"{col} has type {data[col].dtype}, expecting np.int64 or np.float64")
            return False

    # If nothing got caught, the file is internally consistent
    return True


def main(dirpath: str, no_extension: bool):
    """
    Takes a path to a directory and checks whether the ASCII raster
    files in that directory are internally consistent.
    Prints the results to the screen.

    :param dirpath:  Path to a directory of ASCII raster files to check
    :param no_extension: Whether to look for files that don't have an extension
    """
    if no_extension:
        files = find_all(dirpath)
    else:
        files = find_ascii(dirpath)

    # Keep track of how many files were okay
    num_good = 0
    bad_files = []
    # Go through all the files and check whether they are internally consistent
    for candidate in files:
        print(f'\nchecking {os.path.basename(candidate)}...')
        header, df = parse_file(candidate)  # Get the data to compare
        if is_consistent(header, df):
            print(f"{os.path.basename(candidate)} is internally consistent")
            num_good += 1
        else:
            print(f"{os.path.basename(candidate)} is NOT internally consistent")
            bad_files.append(candidate)

    print(f"\nFound {num_good} internally-consistent ASCII raster files out of {len(files)} identified candidates")

    # Alert the user if we found any inconsistent files
    if len(bad_files) > 0:
        print("\nINCONSISTENT FILES FOUND")
        print([os.path.basename(bad_file) for bad_file in bad_files])


if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('filepath', help='Path to a directory containing ASCII raster files to check')
    p.add_argument('-n', '--no-ext', action='store_true',
                   help='Check every file in the directory in order to catch '
                        'ASCII files that do not have a file extension')

    args = p.parse_args()

    main(args.filepath, args.no_ext)
