#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 12:23:44 2022

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


os.chdir('/Users/mcmahon/Repos/CitiBike/Stephanie')

df = pd.read_feather('pidgeon.feather')

df.start_coords = df.start_coords.apply(lambda x: (float(x[0]), float(x[1])))
df.end_coords = df.end_coords.apply(lambda x: (float(x[0]), float(x[1])))

df = df[df.day_type != 'Holidays']

dfA = df[(df.year == 2018) or (df.year == 2019)]

dfB = df[(df.year == 2020) or (df.year == 2021)]




# ignore quiet hours 1am - 5am 
#hours = [0, 6, 7, 8, 9, 10, 11, 12, 13, 14, 
         #15, 16, 17, 18, 19, 20, 21, 22, 23]

#df = df[df21['hour_of_day'].isin(hours)]


# split by day_type



# groupby by start_name and hour_of_day: average ride count





# plots for rider behaviors 


# change in mean duration over the 4 year period
sns.displot(df[df.durationmins < 60], x='durationmins', hue = 'year', 
            kind='kde', bw_adjust=5)

a = sns.displot(data = df, x='hour_of_day', row = 'day_type', col='year', kind = 'kde',  bw_adjust=5)

a.set_axis_labels("Hour of the Day", "Density of Rides")
a.set_titles('2018', '2019', '2020', '2021')


# change in hourly distribution over 4 years
b = sns.displot(data = df, x='hour_of_day', hue = 'user_type', 
                row = 'day_type', col='year', kind = 'kde',  bw_adjust=5)

b.set_axis_labels("Hour of the Day", "Density of Rides")

# change in hourly distribution by user_type
sns.displot(df[df.durationmins < 60], x='durationmins', kind='kde', bw_adjust=2,
            hue = 'user_type', col = 'year', row = 'day_type') 


# duration by day_type and user_type
sns.displot(df[df.durationmins < 60], x='durationmins', kind='kde', bw_adjust=2,
            col = 'year', row = 'day_type') 

sns.displot(data = df, x='month', hue = 'user_type', 
            row = 'day_type', col='year', kind = 'kde',  bw_adjust=5)


