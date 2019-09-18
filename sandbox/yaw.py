import os 
import sys
import zipfile
import exifread
import pandas as pd

zip = sys.argv[1]

latArray = list()
longArray = list()
idCount = 0
idArray = list()
imageName = list()

if os.path.exists(zip) is True:
    zip_ref = zipfile.ZipFile(zip, "r")
    zip_ref.extractall(".")
    zip_ref.close()
    for root, dirs, file in os.walk("."):
        for filename in file:
            if filename.endswith(".jpg"):
                imageExtract = os.path.join(root, filename)
                image = open(imageExtract, "rb")
                tags = exifread.process_file(image, details=False)
                for tag in tags.keys():
                    if tag not in('JPEGTHumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                        # print("\n-------------------------------------------------")
                        # print(filename)
                        # print("Lat",tags['GPS GPSLatitude'])
                        # print("Long",tags['GPS GPSLongitude'])
                        # print(tags['GPS GPSLatitudeRef'].values[0])
                        # print(tags['GPS GPSLongitudeRef'].values[0])
                        # print(tags.keys())
                        latitude = tags["GPS GPSLatitude"]
                        longitude = tags["GPS GPSLongitude"]
                        latDirectionRef = tags['GPS GPSLatitudeRef']
                        longDirectionRef = tags['GPS GPSLongitudeRef']
                        lat = latArray.append(get_decimal_from_dms(latitude, latDirectionRef))
                        lon = longArray.append(get_decimal_from_dms(longitude, longDirectionRef))
                        idArray.append(idCount)
                        imageName.append(filename)
                        idCount+=1
                        break   

        def get_decimal_from_dms(dms, ref):

            degrees = float(dms.values[0].num) / float(dms.values[0].den)
            minutes = float(dms.values[1].num) / float(dms.values[1].den) / 60.0
            seconds = float(dms.values[2].num) / float(dms.values[2].den) / 3600.0

            if ref in ['S', 'W']:
                degrees = -degrees
                minutes = -minutes
                seconds = -seconds

            return round(degrees + minutes + seconds, 5)

# print(latArray)
# print(longArray)
# print(idCount)
# print(idArray)
# print(imageName)
gpsCoordinates = {"id":idArray, "lat":latArray, "long":longArray, "image":imageName}
dfObj = pd.DataFrame(gpsCoordinates)
dfObj.reset_index(drop=True) 
dfObj.to_csv('imageCoordinates.txt', index=False,sep=',')