import pandas as pd
import exifread
from PIL import Image
import os, os.path
from PIL.ExifTags import TAGS, GPSTAGS


# Convert to Degrees function takes the EXIF GPS coordinates and converts them to float form
# From DMS to DD
# Formula: Degrees + (Minutes / 60) + (Seconds / 3600) = Decimal Degrees

def _convert_to_degress(value):

    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

# Function to return a dictionary from Exif data, looking only at GPS information
# converts the GPS Tags using TAGS.get(tag, tag):
    # https://www.programcreek.com/python/example/91518/PIL.ExifTags.TAGS.get

lat_list = []
long_list = []

def get_exif_data(image):
    exif_data = {}
    info = image._getexif()

    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)             # decode the tags
        if decoded == "GPSInfo":                 # Only adds the info with the label GPSInfo
            gps_data = {}                        # Gets rid of a lot of unneccesary data
            for x in value:
                sub_decoded = GPSTAGS.get(x, x)
                gps_data[sub_decoded] = value[x]

                exif_data[decoded] = gps_data


    # only take Latitude and Longitude and their references
    lat = None
    long = None

    gps_info = exif_data["GPSInfo"]

    gps_latitude = gps_info["GPSLatitude"]
    gps_latitude_ref = gps_info['GPSLatitudeRef']
    gps_longitude = gps_info['GPSLongitude']
    gps_longitude_ref = gps_info['GPSLongitudeRef']

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:  #make sure all the vars are there
        lat = _convert_to_degress(gps_latitude)    # use our function to convert from DMS to DD
        if gps_latitude_ref == "S":
            lat = 0 - lat                          # if reference is not N, convert to negative to represent other side of globe

        long = _convert_to_degress(gps_longitude)
        if gps_longitude_ref == "W":
            long = 0 - long                          # same thing, represent other direction

    lat_list.append(lat)                           # append the new lat and long to their respective lists
    long_list.append(long)
    return lat, long


# Read in all the pictures as image1 - image15

# I couldn't get my os.path.expanduser to work so I just wrote in the images the long way

image1 = Image.open("./drive-download-20190916T144006Z-001/image000.jpg", "r")
image2 = Image.open("./drive-download-20190916T144006Z-001/image001.jpg", "r")
image3 = Image.open("./drive-download-20190916T144006Z-001/image002.jpg", "r")
image4 = Image.open("./drive-download-20190916T144006Z-001/image003.jpg", "r")
image5 = Image.open("./drive-download-20190916T144006Z-001/image004.jpg", "r")
image6 = Image.open("./drive-download-20190916T144006Z-001/image005.jpg", "r")
image7 = Image.open("./drive-download-20190916T144006Z-001/image006.jpg", "r")
image8 = Image.open("./drive-download-20190916T144006Z-001/image007.jpg", "r")
image9 = Image.open("./drive-download-20190916T144006Z-001/image008.jpg", "r")
image10 = Image.open("./drive-download-20190916T144006Z-001/image009.jpg", "r")
image11 = Image.open("./drive-download-20190916T144006Z-001/image010.jpg", "r")
image12 = Image.open("./drive-download-20190916T144006Z-001/image011.jpg", "r")
image13= Image.open("./drive-download-20190916T144006Z-001/image012.jpg", "r")
image14= Image.open("./drive-download-20190916T144006Z-001/image013.jpg", "r")
image15 = Image.open("./drive-download-20190916T144006Z-001/image014.jpg", "r")

# Create a list of all the images
image_list = [image1, image2, image3, image4, image5, image6, image7, image8, image9,
              image10, image11, image12, image13, image14, image15]

# Create a pandas data frame with the columns ID, Lat, Long, Name
# Fill the name column with the variable names for each picture
df = pd.DataFrame(columns=( 'Lat', 'Long', 'Name'))
df["Name"] = ["image000.jpg", "image001.jpg", "image002.jpg", "image003.jpg", "image004.jpg", "image005.jpg",
              "image006.jpg", "image007.jpg", "image008.jpg", "image009.jpg", "image010.jpg", "image011.jpg",
              "image012.jpg", "image013.jpg", "image014.jpg"]

df.index.name = 'ID'





for image in image_list:                  # loops through each image, gets the exif data and appends lat and long to   the lists
    get_exif_data(image)

df["Lat"] = lat_list                     # add finished lat and long lists to the dataframe
df['Long'] = long_list

df.to_csv('sandbox_script.csv')         # export to csv file
