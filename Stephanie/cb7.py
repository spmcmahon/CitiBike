#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 18:31:22 2022

@author: mcmahon
"""



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import feather
import os
import random 
from pathlib import Path
import datetime as dt 
#from pandas.tseries.holiday import *


from cb6 import distances 

os.chdir('/Users/mcmahon/Repos/CitiBike/Stephanie')

df = pd.read_feather('CitiBikeSubset.feather')
stations = pd.read_feather('stations.feather')



# convert lats and longs into rounded strings
df['start_lat'] = df['start_lat'].apply(lambda x: '%.6f' %x )
df['start_lng'] = df['start_lng'].apply(lambda x: '%.6f' %x )


df['start_coords'] = list(zip(df['start_lat'], df['start_lng']))


df['end_lat'] = df['end_lat'].apply(lambda x: '%.6f' %x )
df['end_lng'] = df['end_lng'].apply(lambda x: '%.6f' %x )


df['end_coords'] = list(zip(df['end_lat'], df['end_lng']))



# creating new basic features 
df['month'] = df['start_time'].dt.month

df['year'] = df['start_time'].dt.year

# 0-6 starting on Monday
df['day_of_week'] = df['start_time'].dt.weekday 

# pulls integer hour from military time 
df['hour_of_day'] = df['start_time'].dt.hour

# create duration in minuts column 
df['durationmins'] = df['duration'] //60

# drop all rides greater than 24 hrs
df = df.drop(df[df['duration'] > 86400].index)
 
# drop all rides less than 60 seconds
df = df.drop(df[df['duration'] < 60].index)



# convert all coords back to float tuples 
df.start_coords = df.start_coords.apply(lambda x: (float(x[0]), float(x[1])))
df.end_coords = df.end_coords.apply(lambda x: (float(x[0]), float(x[1])))

stations.coords = stations.coords.apply(lambda x: (float(x[0]), float(x[1])))
distances.coords = distances.coords.apply(lambda x: (float(x[0]), float(x[1])))





# merge new station ids, names and regions 
df = df.merge(stations, 
         how = 'left', 
         left_on = 'start_coords', 
         right_on= 'coords', 
         suffixes = (None, '_start')).merge(stations, 
                  how = 'left', 
                  left_on = 'end_coords', 
                  right_on= 'coords', 
                  suffixes = ('_start', '_end'))
                                            
                                            
df.drop(['coords_start', 'coords_end',
         'capacity_start', 'capacity_end'], axis=1, 
        inplace=True)  

df.rename(columns = {'name_start': 'start_name', 'name_end': 'end_name'}, 
          inplace=True)
                                          
                                            
 # merge distance data for start/end stations                                            
df = df.merge(distances, 
         how = 'left', 
         left_on = 'start_coords', 
         right_on= 'coords', 
         suffixes = (None, '_start')).merge(distances, 
                  how = 'left', 
                  left_on = 'end_coords', 
                  right_on= 'coords', 
                  suffixes = ('_start', '_end'))
                                             
                  how = 'left', 
                  left_on = 'end_coords', 
                  right_on= 'coords', 
                  suffixes = ('_start', '_end'))
                                            
                                            
                                            
                                            
df['start_name'].fillna(df['start_station_name'], inplace=True)
df['end_name'].fillna(df['end_station_name'], inplace=True)
df['short_name_start'].fillna(df['start_station_id'], inplace=True)
df['short_name_end'].fillna(df['end_station_id'], inplace=True)




it_like_its_hot = ['lat_start', 'lon_start', 'lat_end', 'lon_end',
'start_station_name', 'start_station_id', 
'end_station_name', 'end_station_id',
'name_start', 'name_end']

df.drop(it_like_its_hot, axis=1, inplace=True)


mic = ['coords_start', 'coords_end']
df.drop(mic, axis=1, inplace=True)

df = df.drop(df[df['subway_dist_start'].isna()].index)
df = df.drop(df[df['subway_dist_end'].isna()].index)


# drop_duplicates ?????


feather.write_dataframe(df, 'notquitethere.feather')

