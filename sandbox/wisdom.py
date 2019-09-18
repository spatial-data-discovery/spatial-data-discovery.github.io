import exifread
import os


def find_files(filepath: str) -> list:
    """
    Finds the files and returns a list of the file paths

    :param filepath: PathLike to a directory of JPEG files
    :return: A list of the JPEG filepaths
    """
    file_list = []

    for root, dirs, files in os.walk(filepath):
        # Put all the paths to JPEG files in the list
        for name in files:
            if name.endswith('.jpg'):
                path = os.path.join(root, name)
                file_list.append(path)
    return file_list


def convert_to_dd(encoded_data: exifread.IfdTag, direction: exifread.IfdTag) -> float:
    """
    Converts the strange exifread format to signed decimal degrees

    :param encoded_data: The list of GPS info from exifread
    :param direction: The direction (N,S, E, W)
    :return: The signed decimal degree version of the location
    """
    exif_list = encoded_data.values
    # Degrees and minutes are stored as an exifread Ratio class, so
    # get the numerator to get the value
    degrees = exif_list[0].num
    minutes = exif_list[1].num
    # The seconds are encoded as a fraction
    # Get the numerator and denominator
    num_seconds = exif_list[2].num
    den_seconds = exif_list[2].den
    deci_seconds = num_seconds / den_seconds
    # Do the conversion
    dd_repr = degrees + (minutes/60) + (deci_seconds/3600)

    if direction.values == "S" or direction.values == "W":
        return -dd_repr
    return dd_repr


def get_loc(filepath: os.PathLike) -> tuple:
    """
    Opens a given JPEG file and uses exifread to return a
    tuple of the (lat, long) metadata in that jpeg

    :param filepath: The path to a JPEG file
    :return: A tuple of (lat, long) in signed decimal degrees
    """
    f = open(filepath, 'rb')  # Open as bytes for exifread
    tags = exifread.process_file(f)
    f.close()

    # Save the lat/long info
    encoded_lat = tags['GPS GPSLatitude']
    lat_dir = tags['GPS GPSLatitudeRef']
    encoded_long = tags['GPS GPSLongitude']
    long_dir = tags['GPS GPSLongitudeRef']

    # Convert the custom exifread format to decimal degrees
    # and get the right sign
    lat = convert_to_dd(encoded_lat, lat_dir)
    long = convert_to_dd(encoded_long, long_dir)

    return lat, long


def build_csv(filepath: str, out_file: str = './out.csv'):
    """
    Build a .csv file with columns ID, LAT, LON, NAME

    :param filepath: A Path to a directory of JPEG files
    :param out_file: A Path for the output .csv file.
                     Defaults to ./out.csv
    """
    file_list = find_files(filepath)
    index = 0
    # Open the output file and write the column names to it
    out_f = open(out_file, 'w')
    out_f.write("ID,LAT,LON,NAME\n")
    for jpg_file in file_list:
        # Get the location data
        lat_long = get_loc(jpg_file)
        lat = lat_long[0]
        long = lat_long[1]
        # Split the path on "/" and take the last element as the name
        name = jpg_file.split('/')[-1]
        # Write the next line of the .csv file
        out_f.write(f"{index},{lat},{long},{name}\n")
        index += 1  # Increment the index
    out_f.close()


if __name__ == "__main__":
    import argparse

    # Parse arguments
    p = argparse.ArgumentParser()
    p.add_argument("filepath", help="The path to a directory of JPEG files")
    p.add_argument("-o", "--out", nargs='?', default="./out.csv", help="Optional path to an output file")
    args = p.parse_args()

    # Build the .csv file
    build_csv(args.filepath, args.out)
