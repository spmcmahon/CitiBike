#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 17:59:20 2022

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

def make_year(folder, newname):
    os.chdir(folder)
    data = {'start_time' : pd.Series([], dtype ='datetime64[ns]'),
    'end_time' : pd.Series([], dtype ='datetime64[ns]'),
    'duration' : pd.Series([], dtype ='int32'),
    'start_station_name' : pd.Series([], dtype = 'str'),
    'start_station_id' : pd.Series([], dtype = 'str'),
    'end_station_name' : pd.Series([], dtype = 'str'),
    'end_station_id' : pd.Series([], dtype = 'str'),
    'start_lat' : pd.Series([], dtype = 'float64'),
    'start_lng' : pd.Series([], dtype = 'float64'), 
    'end_lat' : pd.Series([], dtype = 'float64'),
    'end_lng' : pd.Series([], dtype = 'float64'), 
    'user_type': pd.Series([], dtype = 'category')}
    
    year = pd.DataFrame(data)
    
    for file in os.listdir(folder): 
        if '-clean.feather' not in file:
            continue
        # read in clean feather file
        month = pd.read_feather(file)
        
        # concat years together 
        year = pd.concat([year, month], axis = 0, ignore_index=True)
        print(year.shape)
       
      
        
    feather.write_dataframe(year, newname)
    return year
  

subfolder = '/Users/mcmahon/Repos/CitiBike/Stephanie/Data Files/NewYork/NY2021'
NY21 = make_year(subfolder, 'NY2021.feather')




    