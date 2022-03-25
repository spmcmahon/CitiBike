#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 10:04:49 2022

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


os.chdir('/Users/mcmahon/Repos/CitiBike/Stephanie/Data Files/NewYork/Subsets')
df = pd.read_feather('CitiBikeSubset.feather')



# drop empty start station  (3)
# drop duration < 60 (135K) 
# drop duration > 86400 (6K)




df['month'] = df['start_time'].dt.month

df['year'] = df['start_time'].dt.year

# 0-6 starting on Monday
df['day_of_week'] = df['start_time'].dt.weekday 

# pulls integer hour from military time 
df['hour_of_day'] = df['start_time'].dt.hour

def Day_type(df):
    df["day_type"] = df["start_time"].dt.weekday
    df["day_type"] = np.where(df["day_type"] > 4, "Weekend","Weekday")
    sdt = df["start_time"].iat[0].strftime("%Y-%m-%d")
    edt = df["start_time"].iat[-1].strftime("%Y-%m-%d")
    cal = USFederalHolidayCalendar()
    holidays = cal.holidays(start=sdt, end=edt).strftime("%Y-%m-%d")
    df.loc[df['start_time'].dt.strftime("%Y-%m-%d").isin(holidays), 'day_type'] = 'Holidays'


Day_type(df)



# if we ever get weather data for 2020/21 - merge on closest time
#df.merge_asof(weather, left_on = , right_on = , direction = 'nearest')



# get zipcode from lat/long 
# df['start_zip']
# df['end_zip']


bus = pd.read_csv('citibike_bus_distances.csv')
subway = pd.read_csv('citibike_subway_distances.csv')
park = pd.read_csv('park_distances.csv')
poly = pd.read_csv('citibike_polygon.csv')




# create sub dataframes for start/end stations with their lat & long
starts = df[['start_station_name', 'start_lat', 'start_lng']]
ends = df[['end_station_name', 'end_lat', 'end_lng']]


starts.drop_duplicates(subset=['start_station_name'],inplace=True,ignore_index=True)
ends.drop_duplicates(subset=['end_station_name'],inplace=True,ignore_index=True)
starts.dropna(axis=0, inplace=True)



start2 = df[['start_station_name', 'start_station_id', 'start_lat', 'start_lng']]
end2= df[['end_station_name', 'end_station_id', 'end_lat', 'end_lng']]

start2.dropna(axis=0, inplace=True)
start2.drop_duplicates(subset=['start_station_name'], keep='first', inplace=True,ignore_index=True)


start2.start_station_id.value_counts(sort=True).head()


5190.09    3
7039.03    2
4781.05    2
7837.3     2
5679.08    2
4488.09    2
3427.0     2
6708.04    2
6122.09    2
3466       2
6662.08    2
5382.07    2
2782.02    2



6708.04    2
5679.08    2
5190.09    2
6122.09    2

start2.loc[start2['start_station_id'] == '6708.04']
start2.loc[start2['start_station_id'] == '5679.08']
start2.loc[start2['start_station_id'] == '5190.09']
start2.loc[start2['start_station_id'] == '6122.09']

start2.


start2.drop_duplicates(subset=['start_lat', 'start_lng'], keep='first', inplace=True,ignore_index=True)

#Broadway & W 48th St
start2.loc[1554, 'start_station_name'] = 'Broadway & W 48th St'
start2.loc[1574, 'start_station_name'] = 'Broadway & W 48th St'

# Bleeker St & Layfayette St
start2.loc[1549,'start_station_name'] = 'Bleeker St & Layfayette St'
start2.loc[1648,'start_station_name'] = 'Bleeker St & Layfayette St'

# Clinton St & Cherry St
start2.loc[856,'start_station_name'] = 'Clinton St & Cherry St'
start2.loc[1565,'start_station_name'] = 'Clinton St & Cherry St'

# 2 Ave & E 29 St
start2.loc[1137,'start_station_name'] = '2 Ave & E 29 St'
start2.loc[1649,'start_station_name'] = '2 Ave & E 29 St'


start2.drop_duplicates(subset=['start_station_name'], keep='first', inplace=True,ignore_index=True)




# start station names to be dropped (all rides)
1640                                            HB409*
1645                                      MTL-ECO51-1*
1646    S 5th St & Kent Ave (Domino Park Movie Shoot)*
1638                                           SYS032*
1630                                           SYS052*


start2.start_station_id = start2.start_station_id.astype(float)

start2.start_station_id == 'HB409'
start2.start_station_id == 'MTL-ECO51-1'
start2.start_station_id == 'S 5th St & Kent Ave (Domino Park Movie Shoot)'
start2.start_station_id == 'SYS032'
start2.start_station_id == 'SYS052'


badids = ['HB409', 'MTL-ECO51-1', 'S 5th St & Kent Ave (Domino Park Movie Shoot)',
          'SYS032', 'SYS052'] 


start2.drop(start2[start2['start_station_id']=='HB409'].index, inplace=True) 
start2.drop(start2[start2['start_station_id']=='MTL-ECO51-1'].index, inplace=True)
start2.drop(start2[start2['start_station_id']=='S 5th St & Kent Ave (Domino Park Movie Shoot)'].index, inplace=True)
start2.drop(start2[start2['start_station_id']=='SYS032'].index, inplace=True)
start2.drop(start2[start2['start_station_id']=='SYS052'].index, inplace=True)


start2['start_coords'] = list(zip(start2['start_lat'], start2['start_lng']))


feather.write_dataframe(start2, 'start_stations.feather')

end2.drop_duplicates(subset=['end_station_name'], keep='first', inplace=True,ignore_index=True)
end2.drop_duplicates(subset=['end_lat', 'end_lng'], keep='first', inplace=True,ignore_index=True)

end2.end_station_id.value_counts(sort=True).head()


6122.09    2
6708.04    2
5382.07    2
5190.09    2
4488.09    2

#Broadway & W 48th St
end2.loc[1592, 'end_station_name'] = 'Broadway & W 48th St'
end2.loc[1655, 'end_station_name'] = 'Broadway & W 48th St'

# Boerum Pl & Pacific St
end2.loc[1521,'end_station_name'] = 'Boerum Pl & Pacific St'
end2.loc[1665,'end_station_name'] = 'Boerum Pl & Pacific St'

# Clinton St & Cherry St
end2.loc[873,'end_station_name'] = 'Clinton St & Cherry St'
end2.loc[1484,'end_station_name'] = 'Clinton St & Cherry St'

# 2 Ave & E 29 St
end2.loc[895,'end_station_name'] = '2 Ave & E 29 St'
end2.loc[1687,'end_station_name'] = '2 Ave & E 29 St'

# Forsyth St & Grand St
end2.loc[909, 'end_station_name'] = 'Forsyth St & Grand St'
end2.loc[1158, 'end_station_name'] = 'Forsyth St & Grand St'

end2.drop_duplicates(subset=['end_station_name'], keep='first', inplace=True,ignore_index=True)

# people like to take bikes from NYC to Jersey apparently 
# 54 to HB and 73 to JC total from df 
# 267 to SYS stations 
1666                                            HB102
1671                                            HB103
1661                                            HB201
1665                                            HB202
1563                                            HB203
1670                                            HB302
1694                                            HB304
1693                                            HB402
1674                                            HB403
1696                                            HB404
1678                                            HB409
1668                                            HB502
1690                                            HB505
1673                                            HB506
1686                                            HB507
1689                                            HB602
1675                                            JC006
1677                                            JC013
1676                                            JC032
1684                                            JC034
1623                                            JC055
1669                                            JC065
1685                                            JC077
1695                                            JC081
1660                                            JC082
1692                                            JC094
1664                                            JC095
1683                                            JC096
1559                                            JC098
1565                                            JC102
1691                                            JC103
1566                                            JC106
1561                                        Lab - NYC
1682                                      MTL-ECO51-1
1688    S 5th St & Kent Ave (Domino Park Movie Shoot)
1662                                           SYS016
1650                                           SYS032
1564                                           SYS033
1397                                           SYS035
1687                                           SYS038
1655                                           SYS052

end2.drop(end2[end2['end_station_id'].str.startswith('HB')].index, inplace=True)
end2.drop(end2[end2['end_station_id'].str.startswith('JC')].index, inplace=True)
end2.drop(end2[end2['end_station_id'].str.startswith('SYS')].index, inplace=True)
end2.drop(end2[end2['end_station_id'].str.startswith('MTL')].index, inplace=True)
end2.drop(end2[end2['end_station_id'].str.startswith('Lab')].index, inplace=True)
end2.drop(end2[end2['end_station_id'].str.startswith('S 5th St & Kent Ave (Domino Park Movie Shoot)')].index, inplace=True)

end2['end_coords'] = list(zip(end2['end_lat'], end2['end_lng']))

feather.write_dataframe(end2, 'end_stations.feather')

start_end = end2.merge(start2, how = 'outer', left_on = 'end_coords', right_on = 'start_coords')
