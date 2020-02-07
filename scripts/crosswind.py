# crosswind.py
#
# Author: Grant Luisi
#
# Date: 2020-02-07
#
# This script calculates which runway should be used based
# on the wind and calculates the crosswind component
# Required Modules
from math import sin, radians
import argparse

# Function

def crosswind():
    r = int(input('Enter a runway number (1-36): '))
    d = int(input('Enter wind direction in degrees (1-360): '))
    s = int(input('Enter wind velocity: '))
    try:
        # determining runways
        first_runway = r
        if first_runway <= 18:
            second_runway = r+18
        else:
            second_runway = r-18
        # determining the desired runway
        first_runway = first_runway*10
        second_runway = second_runway*10
        first_runway_degree_crosswind = abs(d-first_runway)
        second_runway_degree_crosswind = abs(d-second_runway)
        if first_runway_degree_crosswind>second_runway_degree_crosswind:
            desired_runway = second_runway
        else:
            desired_runway = first_runway
        # Calculating crosswind component if intial runway is preferred
        if desired_runway == first_runway:
            crosswind_component = s*sin(radians(first_runway_degree_crosswind))
            print('Use runway '+str(first_runway/10)+'. The crosswind component is '+str(crosswind_component))
        # Calculating crosswind component if other runway is preferred
        elif desired_runway == second_runway:
            crosswind_component = s*sin(radians(second_runway_degree_crosswind))
            print('Instead of your intial runway, use runway '+str(second_runway/10)+'. The crosswind_component is '+str(crosswind_component))
    except ValueError:
        print('Oops')

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Calculates which runway to use and the associated crosswind component")
    args = p.parse_args()
    crosswind()
