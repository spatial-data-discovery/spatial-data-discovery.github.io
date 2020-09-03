# Andrew Caietti
#
# live_aviation.py
#
# Recent Edit: 2020-09-03
#
# This script calls an opensource API from OpenSkyNetwork.com. 
# The data can then be saved as a CSV or worked with in its converted two-dimensional
# array format. Each sub-array represents an individual aircraft with 
# 17 total fields.



##################
# MODULES NEEDED #
##################
import pandas as pd
from opensky_api import OpenSkyApi 
import argparse
from time import gmtime, strftime
from tkinter.filedialog import askdirectory

###############
#  Functions  #
###############


# Generate the a 2-dimensional array where each sub-array is an individual aircraft
def RetrievePlaneData(): 
    api = OpenSkyApi()  # Call the API
    states = api.get_states()
    main_array = []
    for s in states.states: # Iterate through and store states object attributes (StateVector)
        temp_array=[0]*17
        temp_array[0]=s.icao24
        temp_array[1]=s.callsign
        temp_array[2]=s.origin_country
        temp_array[3]=s.time_position
        temp_array[4]=s.last_contact
        temp_array[5]=s.longitude
        temp_array[6]=s.latitude
        temp_array[7]=s.baro_altitude
        temp_array[8]=s.velocity
        temp_array[9]=s.heading
        temp_array[10]=s.vertical_rate
        temp_array[11]=s.on_ground
        temp_array[12]=s.sensors 
        temp_array[13]=s.geo_altitude
        temp_array[14]=s.squawk
        temp_array[15]=s.spi   
        temp_array[16]=s.position_source       
        main_array.append(temp_array)
    return main_array   


# Pass a path name, where you would like to save the file, and the data you called from RetrievePlaneData, to generate a CSV file on your desktop.
def PlaneDatatoCSV(path_name,data):
    df = pd.DataFrame(data) 
    df.columns = ['icao24','Callsign','Origin Country','Time Position','Last Contact','Longitude','Latitude','Baro Altitude','Velocity','Heading','Vertical Rate','On Ground','Sensors','Geo Altitude','Squawk','Spi','Position Source']
    ts = strftime(r'%Y_%m_%d__%H_%M_%S') # Record current time to time-stamp the file
    df.to_csv(path_name+r"\Aviation_Data__"+ts+r'.csv',index=False,header=True)
    

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description="Retrieve live, open-source aviation data about what planes are flying where in the world.")
    parser.add_argument('--link', default = 'https://opensky-network.org/', help='Link to the API (datasource).')
    args = parser.parse_args()

current_data = RetrievePlaneData()
my_path = askdirectory(title='Select Folder') # Allow user to choose what folder to save data in
PlaneDatatoCSV(my_path,current_data)


        
 






