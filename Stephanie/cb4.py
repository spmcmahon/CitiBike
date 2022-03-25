#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 10:06:15 2022

@author: mcmahon
"""

import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import feather


url = 'https://gbfs.citibikenyc.com/gbfs/en/station_information.json'



#Get JSON with Requests
def _getDataFramefromURL(url, entity, index):
    response = requests.request("GET", url)
    json_response = json.loads(response.text)
    df_temp = pd.DataFrame(json_normalize(json_response['data'][entity]))
    df_temp = df_temp.set_index(index) 
    return df_temp

# Get static data from CitiBike from URL
url_station_info = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
url_system_regions = "https://gbfs.citibikenyc.com/gbfs/en/system_regions.json"

df_station_info = _getDataFramefromURL(url_station_info, 'stations', 'station_id')
df_system_regions = _getDataFramefromURL(url_system_regions, 'regions', 'region_id')


# has_kiosk                            bool
# legacy_id                          object
# *name                               object
# *capacity                            int64
# rental_methods                     object
# *short_name                         object
# *lat                               float64
# *lon                               float64
# electric_bike_surcharge_waiver       bool
# external_id                        object
# *region_id                          object
# eightd_station_services            object
# eightd_has_key_dispenser             bool
# station_type                       object
# rental_uris.ios                    object
# rental_uris.android                object


stations = df_station_info[['name', 'capacity', 'short_name', 'lat', 'lon', 'region_id']]

stations.reset_index(inplace=True)
stations.drop(columns=['station_id'], axis=1, inplace = True)

stations['lat'] = stations['lat'].apply(lambda x: '%.6f' %x )
stations['lon'] = stations['lon'].apply(lambda x: '%.6f' %x )


stations['coords'] = list(zip(stations['lat'], stations['lon']))
                            
feather.write_dataframe(stations, 'stations.feather')






