# Andrew Caietti
#
# live_aviation.py
#
# Last Updated: 2020-11-17


##### Summary #####

# This script calls an opensource API from OpenSkyNetwork.com. 
# The data can then be saved as a CSV or worked with in its pandas dataframe
# format. Each row represents an individual aircraft with 
# 17 total fields.
#
# For further information, please see the link below (valied as of 2020-11-17)
# https://opensky-network.org/
###################


##################
# MODULES NEEDED #
##################
import pandas as pd
from opensky_api import OpenSkyApi 
import argparse
from time import gmtime, strftime, sleep
import os

###############
#  Functions  #
###############


def RetrievePlaneData_Full(): 
    """
    Name:       RetrievePlaneData_Full
    Outputs:    Aviation data in a Pandas Dataframe
    Features:   Call the Opensky-network API and retrieve all possible data
                and return a Pandas Dataframe of the data.
    Note:       API call has 15 second requirement between calls. This function will
                sleep if the API is called too quickly.
    """
    # Call the API and full data
    while True:
        try:            
            api = OpenSkyApi()  
            states = api.get_states()
            break
        except:
            # Occasionally, the API can reject a request (15 second necessary time between requests)
            # If error arises, sleep the necessary time and try again
            sleep(15)
    
    main_array = []
    for item in states.states:
    # Iterate through and store states object attributes (StateVector) 
        temp_array=[0]*17
        temp_array[0]=item.icao24
        temp_array[1]=item.callsign
        temp_array[2]=item.origin_country
        temp_array[3]=item.time_position
        temp_array[4]=item.last_contact
        temp_array[5]=item.longitude
        temp_array[6]=item.latitude
        temp_array[7]=item.baro_altitude
        temp_array[8]=item.velocity
        temp_array[9]=item.heading
        temp_array[10]=item.vertical_rate
        temp_array[11]=item.on_ground
        temp_array[12]=item.sensors 
        temp_array[13]=item.geo_altitude
        temp_array[14]=item.squawk
        temp_array[15]=item.spi   
        temp_array[16]=item.position_source       
        main_array.append(temp_array)
    
    # Create and formate dataframe for use
    aviation_df = pd.DataFrame(main_array)
    aviation_df.columns = ['icao24','Callsign','Origin Country','Time Position',
    'Last Contact','Longitude','Latitude','Baro Altitude','Velocity','Heading','Vertical Rate',
    'On Ground','Sensors','Geo Altitude','Squawk','Spi','Position Source']

    return aviation_df   




# Pass a path name, where you would like to save the file, and the data you called from RetrievePlaneData, 
# to generate a file on your desktop, default type being CSV
def PlaneData_to_file(file_name,df, save_folder=os.path.dirname(os.path.realpath(__file__)), save_type='csv'):
    """
    Name:       PlaneData_to_file
    Inputs:     - str, name of file to be saved (file_name)
                - dataframe, dataframe of aviation data (data)
                OPTIONAL
                    - str, change location of ouput file (save_folder)
                    - str, specifies what format to store data in (save_type)
                        -- supported formates include: csv, json, hdf, excel
    Outputs:    File saved as file_name in the current directory
    Features:   Creates a time-stamped file of live aviation dataframe, default is CSV format

    """

    # Check if mandatory arguments are valid
    if type(file_name) is str and isinstance(df, pd.DataFrame):

        # Check to see if optional save folder is a valid string and valid directory
        if type(save_folder) is str or bytes:
            if os.path.isdir(save_folder) is not True:
                print('ERROR: save_folder could not be found as a valid directory\n')
                return

        else:
            save_folder = os.path.dirname(os.path.realpath(__file__))
        
        temp_save_path = os.path.join(save_folder, file_name)
        timestamp = strftime(r'%Y-%m-%d__H%H-M%M-S%S') # Record current time to time-stamp the file

        # Check if save_type is valid, then the save file according to given save_type
        if type(save_type) is str:
            if save_type == 'csv':
                final_save_path = temp_save_path + timestamp+r'.csv'
                df.to_csv(final_save_path,index=False,header=True)
            elif save_type == 'json':
                final_save_path = temp_save_path + timestamp+r'.json'
                df.to_json(final_save_path)
            elif save_type == 'hdf':
                final_save_path = temp_save_path + timestamp+r'.h5'
                df.to_hdf(final_save_path, 'data')
            elif save_type == 'excel':
                final_save_path = temp_save_path + timestamp+r'.xlsx'
                df.to_excel(final_save_path)            
        else:
            print("ERROR: save_type argument is not string.\n Tip: save_type arguments include: json, csv, hdf, excel")

    else:

        # Check which or if both arguments failed
        if type(file_name) is not str:
            print('ERROR: file_name not recognized as string\n')
        if isinstance(df, pd.DataFrame) is not True:
            print('ERROR: data not recognized as pandas dataframe\n')
    

if __name__ =='__main__':
    description = """Retrieve live, open-source aviation data about\n 
    what planes are flying where in the world. This script does so by\n
    providing a function (RetrievePlaneData_Full) to extract a pandas\n
    dataframe of the OpenSky Aviation data, and a function (PlaneData_to_file)\n
    to write that dataframe to a file on your machine."""

    parser = argparse.ArgumentParser(description=description)
    args = parser.parse_args()


    current_data = RetrievePlaneData_Full()
    PlaneData_to_file(file_name = 'OPENSKY_aviation_data_', df=current_data)
    


        
 






