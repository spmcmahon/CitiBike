
#import * from geodatacleaning.py

# Import required modules 
import geopandas
import geopy.distance
from geopy.distance import geodesic
import geopy
import time
from shapely.geometry import Polygon, Point


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import feather
import os
import random 
from pathlib import Path
import datetime as dt 




os.chdir('/Users/mcmahon/Repos/CitiBike/Stephanie')

busdf = pd.read_csv('Bus_Stop_Shelter.csv')
stations = pd.read_feather('stations.feather')

stations.coords = stations.coords.apply(lambda x: (float(x[0]), float(x[1])))

# getting bus station coordinates 
busdf['coords'] = list(zip(busdf['LATITUDE'],busdf['LONGITUDE']))
busdf.drop_duplicates(subset = ['SHELTER_ID'],inplace =True)


# bus distances

busdistances = []


for z,i in enumerate(stations.coords):
    busdistances.clear()
        
    for x in busdf.coords:
        busdistances.append(geodesic(x,i).miles)
       
    stations.loc[z,'bus_distances']=(min(busdistances))
    
endbusdistances = []




