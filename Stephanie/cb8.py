#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 10:57:05 2022

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
from pandas.tseries.holiday import *
import math



os.chdir('/Users/mcmahon/Repos/CitiBike/Stephanie')

df = pd.read_feather('notquitethere.feather')

df.drop_duplicates(subset = ['start_time', 'end_time'], 
                   inplace=True, ignore_index=True)

def Day_type(df):
    df["day_type"] = df["start_time"].dt.weekday
    df["day_type"] = np.where(df["day_type"] > 4, "Weekend","Weekday")
    sdt = df["start_time"].iat[0].strftime("%Y-%m-%d")
    edt = df["start_time"].iat[-1].strftime("%Y-%m-%d")
    cal = USFederalHolidayCalendar()
    holidays = cal.holidays(start=sdt, end=edt).strftime("%Y-%m-%d")
    df.loc[df['start_time'].dt.strftime("%Y-%m-%d").isin(holidays), 'day_type'] = 'Holidays'


Day_type(df)

df.year = df.year.astype('category')










