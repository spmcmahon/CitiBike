#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:23:13 2022

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

os.chdir('/Users/mcmahon/Repos/CitiBike/Stephanie')

df = pd.read_feather('CitiBikeSubset.feather')
stations = pd.read_feather('stations.feather')

# cleaning df 




# map over start/end name & id with stations dictionary 

# after mapping, drop null values (stations not in dictionary)




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



# merged with startions on start 
df2 = df.merge(stations, 
         how = 'left', 
         left_on = 'start_coords', 
         right_on= 'coords', 
         suffixes = (None, '_start'))


# start stations that no longer exist 
oldstats = df2.loc[df2.name.isna()][['start_station_name', 'start_coords']]
oldstats.drop_duplicates(inplace=True, ignore_index=True)
oldstats.dropna(axis=0, inplace=True)
oldstats.drop_duplicates(subset = ['start_station_name'], inplace=True, ignore_index=True)

feather.write_dataframe(oldstats, 'old_stations.feather')




# og merged with stations on end 
df3 = df.merge(stations, 
         how = 'left', 
         left_on = 'end_coords', 
         right_on= 'coords', 
         suffixes = ('_start', '_end'))

# find end stations that no longer exist 
oldstats2 = df3.loc[df3.name.isna()][['end_station_name', 'end_coords']]
oldstats2.drop_duplicates(inplace=True, ignore_index=True)
oldstats2.drop_duplicates(subset = ['end_station_name'], inplace=True, ignore_index=True)

feather.write_dataframe(oldstats2, 'more_old_stations.feather')


# merge og to stations twice : first on start, then on end 

df4 = df.merge(stations, 
         how = 'left', 
         left_on = 'start_coords', 
         right_on= 'coords', 
         suffixes = (None, '_start')).merge(stations, 
                  how = 'left', 
                  left_on = 'end_coords', 
                  right_on= 'coords', 
                  suffixes = ('_start', '_end'))
                                            
                                            
DNE = oldstats.merge(oldstats2, how = 'outer', 
                     left_on= 'start_coords', 
                     right_on= 'end_coords')            
