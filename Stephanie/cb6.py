#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 17:59:30 2022

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


start = pd.read_feather('old_stations_nozip.feather')

end = pd.read_feather('end_old_stations.feather')

current = pd.read_feather('stations_with_features.feather')

curr_cols = { 'subway_distances': 'subway_dist', 
              'bus_distances' : 'bus_dist', 
              'park_distances' :'park_dist', 
              'Commercial_distances' : 'comm_dist'}

drop_cols = ['start_Zipcode', 'short_name',
             'lat', 'lon', 'region_id', 'capacity']

current.rename(columns = curr_cols, inplace=True)
current.drop(drop_cols, axis=1, inplace = True)



start_cols = {'start_station_name' : 'name', 
              'start_coords' : 'coords', 
              'subway_distances': 'subway_dist', 
              'bus_distances' : 'bus_dist', 
              'park_distances' :'park_dist', 
              'Commercial_distances' : 'comm_dist'}


start.rename(columns = start_cols, inplace=True)
start.drop('start_zipcode', axis=1, inplace = True)

end_cols = {'end_station_name' : 'name', 
              'end_coords' : 'coords', 
              'subway_distances': 'subway_dist', 
              'bus_distances' : 'bus_dist', 
              'park_distances' :'park_dist', 
              'Commercial_distances' : 'comm_dist'}




end.rename(columns = end_cols, inplace = True)

distances = pd.concat([start, end, current], 
                      axis=0, 
                      ignore_index=True)

