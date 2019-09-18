#!/usr/bin/env python3
#
# VERSION 0.1
#
# LAST EDIT: 2019-09-17
#
# For GPS data challenge
#
##############################################################################
# REQUIRED MODULES
##############################################################################
import exifread
import os
import csv

##############################################################################
# CLASSES
##############################################################################
class GPS(object):
    """
    Name:     GPS
    Features: Scrape GPS info from jpgs
    History:  Version 0.1
              - Written for class
              - written in a hurry so not v nicely formatted sorry
              - TBH I am not sure how accurate the coordinates are
    """

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Class Initialization
    # ////////////////////////////////////////////////////////////////////////
    def __init__(self, base_dir):
        """
        Name:       GPS.__init__
        Inputs:     str, base directory (base_dir)
        Features:   Initializes the GPS class
        Reference:  Way of checking directory is from Prof. Davis's music_randomizer
        """
        self.lat_dms = 0
        self.lon_dms = 0
        self.lat_val = 1
        self.lon_val = 1
        if os.path.isdir(base_dir):
            self.base_dir = base_dir
        else:
            self.base_dir = None
            raise OSError("Directory '%s' does not exist" % (base_dir))

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Class Function Definitions
    # ////////////////////////////////////////////////////////////////////////
    def dms_to_dd(self, dms, ref):
        # DMS presented as [36, 24, 3027/100]
        # shout out to Jiaying, I did not know to do .values[0].num
        degrees = float(dms.values[0].num)
        minutes = float(dms.values[1].num)
        seconds = float(dms.values[2].num)
        dd = (degrees) + (minutes)/60 + (seconds)/3600
        dd = dd * ref
        return dd

    def get_tags(self, file):
        # shout out to Jiaying, I did not know how to look for .values[0]
        if file.endswith(".jpg") or file.endswith(".jpeg"):
            f = open(file, 'rb')
            tags = exifread.process_file(f)
        for tag in tags.keys():
            if tag in ('GPS GPSLatitude'):
                self.lat_dms = tags[tag]
            elif tag in ('GPS GPSLongitude'):
                self.lon_dms = tags[tag]
            elif tag in ('GPS GPSLatitudeRef'):
                lat_ref = tags[tag].values[0]
            elif tag in ('GPS GPSLongitudeRef'):
                lon_ref = tags[tag].values[0]
        if lat_ref == 'N':
            self.lat_val = -1
        if lon_ref == 'E':
            self.lon_val = -1

    def run(self, base_dir):
        os.chdir(base_dir)
        with open('./gps_data.csv', mode='w') as gps_file:
            gps_writer = csv.writer(gps_file, delimiter=',')
            gps_writer.writerow(['ID', 'LAT', 'LON', 'NAME'])
        index = 0
        for file in os.listdir(base_dir):
            if file.endswith(".jpg") or file.endswith(".jpeg"):
                self.get_tags(file)
                longitude = self.dms_to_dd(self.lon_dms, self.lon_val)
                latitude = self.dms_to_dd(self.lat_dms, self.lat_val)
                with open('./gps_data.csv', mode='a') as gps_file:
                    gps_writer = csv.writer(gps_file, delimiter=',')
                    gps_writer.writerow([index, longitude, latitude, file])
                index += 1

##############################################################################
# MAIN
##############################################################################
if __name__ == "__main__":
    input_path = str(input("Type path to directory: "))
    scraper = GPS(input_path)
    scraper.run(input_path)
