import exifread
import os
import pandas as pd

def _convert_to_decimal(dms):
    d = float(dms.values[0].num)/float(dms.values[0].den)
    m = float(dms.values[1].num) / float(dms.values[1].den)
    s = float(dms.values[2].num) / float(dms.values[2].den)
    return d + (m/60) + (s/3600)

def _convert_direction(la,lo,ns,ew):
    if ns == 'S':
       la = la * (-1)
    if ew == 'W':
       lo = lo * (-1)
    return la, lo

def find_location(filepath):
    f = open(filepath,'rb')
    tags = exifread.process_file(f,details=False)
    la_dms = tags['GPS GPSLatitude']
    lo_dms = tags['GPS GPSLongitude']
    ns = tags['GPS GPSLatitudeRef'].values[0]
    ew = tags['GPS GPSLongitudeRef'].values[0]
    la = _convert_to_decimal(la_dms)
    lo = _convert_to_decimal(lo_dms)
    return  _convert_direction(la,lo,ns,ew)

path = input('Enter the path(folder):')
filenames = os.listdir(os.path.expanduser(path))
la_list = [None]*len(filenames)
lo_list = [None]*len(filenames)
i = 0
for file in filenames:
    filepath = os.path.expanduser(path) + '/' + file
    la_list[i], lo_list[i]= find_location(filepath)
    i += 1
data = {'LAT':la_list, 'LON':lo_list}
df = pd.DataFrame(data)
df.index.names = ['ID']
df['NAME'] = filenames
df.to_csv('ImageGPS.txt', index=True,sep=' ')
