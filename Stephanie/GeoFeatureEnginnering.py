# Feature Enginnerring 


import * from geodatacleaning.py

# Import required modules 
import geopandas
import geopy.distance
from geopy.distance import geodesic
import geopy
import time
from shapely.geometry import Polygon, Point



# subway distances 

startdistances = []


for z,i in enumerate(starts.coords):
    startdistances.clear()
        
    for x in subwaydf.the_geom:
        startdistances.append(geodesic(x,i).miles)
      
    starts.loc[z,'subway_distances']=(min(startdistances))



enddistances = []


for z,i in enumerate(ends.coords):
    enddistances.clear()
        
    for x in subwaydf.the_geom:
        enddistances.append(geodesic(x,i).miles)
      
    ends.loc[z,'subway_distances']=(min(enddistances))


# bus distances

busdistances = []


for z,i in enumerate(starts.coords):
    busdistances.clear()
        
    for x in busdf.coords:
        busdistances.append(geodesic(x,i).miles)
       
    starts.loc[z,'bus_distances']=(min(busdistances))
    
endbusdistances = []


for z,i in enumerate(ends.coords):
    endbusdistances.clear()
        
    for x in busdf.coords:
        endbusdistances.append(geodesic(x,i).miles)
       
    ends.loc[z,'bus_distances']=(min(endbusdistances))



# park distances 

parkdist =[]


for z,i in enumerate(starts.coords):
    parkdist.clear()
    temp = i
    for x in parkspolys: 
    
        t = geopandas.GeoSeries(x)
        t2 = geopandas.GeoSeries(Point(temp))
        
        parkdist.append(t.distance(t2)[0])
        
    starts.loc[z,'park_distances'] = min(parkdist)

for z,i in enumerate(ends.coords):
    parkdist.clear()
    temp = i
    for x in parkspolys: 
    
        t = geopandas.GeoSeries(x)
        t2 = geopandas.GeoSeries(Point(temp))
        
        parkdist.append(t.distance(t2)[0])
       
    ends.loc[z,'park_distances'] = min(parkdist)



# high traffic areas 

starts['high_traffic'] = 0

for z,i in enumerate(starts.coords):
    for x in polygonlist_:
        if  Point(i).within(x) == True: 
            starts.loc[z,'high_traffic'] = 1 
            break

ends['high_traffic'] = 0

for z,i in enumerate(ends.coords):
    for x in polygonlist_:
        if  Point(i).within(x) == True: 
            ends.loc[z,'high_traffic'] = 1 
            break


# distances from high traffic polygons

alldist =[]
polygondist = []

for z,i in enumerate(starts.coords):
    alldist.clear()
    temp = i
    for x in polygonlist_: 
    
        t = geopandas.GeoSeries(x)
        t2 = geopandas.GeoSeries(Point(temp))
    
        alldist.append(t.distance(t2)[0])
    starts.loc[z,'poly_distances'] = min(alldist)
    print(min(alldist))
    
for z,i in enumerate(ends.coords):
    alldist.clear()
    temp = i
    for x in polygonlist_: 
    
        t = geopandas.GeoSeries(x)
        t2 = geopandas.GeoSeries(Point(temp))
    
        alldist.append(t.distance(t2)[0])
    ends.loc[z,'poly_distances'] = min(alldist)


# zip codes 


geolocator = geopy.Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',timeout =10)


for z,i in enumerate(starts.coords):
    time.sleep(1)
    location = geolocator.reverse(i)
    print(location.raw['address']['postcode'])
    starts[z,'start_Zipcode']= location.raw['address']['postcode']

for z,i in enumerate(ends.coords):
    time.sleep(1)
    location = geolocator.reverse(i)
    print(location.raw['address']['postcode'])
    ends[z,'start_Zipcode']= location.raw['address']['postcode']



    


 
    


