# Reading and cleaning subset data for features 

uniquestationdf = pd.read_feather("NY2021_sub25.feather") 

# Seperating start and end stations
starts = uniquestationdf[['start_station_name', 'start_lat', 'start_lng']]
ends = uniquestationdf[['end_station_name', 'end_lat', 'end_lng']]

# getting unique stations 
starts.drop_duplicates(subset=['start_station_name'],inplace=True,ignore_index=True)
ends.drop_duplicates(subset=['end_station_name'],inplace=True,ignore_index=True)
starts.dropna(axis=0, inplace=True)
ends.dropna(axis=0, inplace = True)


# Getting Coordinate Columns
starts['coords'] = list(zip(starts['start_lat'],starts['start_lng']))

ends['coords'] = list(zip(ends['end_lat'],ends['end_lng']))

# loading subway data for coordinates 
subwaydf = pd.read_csv("DOITT_SUBWAY_STATION_01_13SEPT2010.csv")

# cleaning subway coordinate columns 

subwaydf.the_geom = subwaydf.the_geom.map(lambda string: string.strip('POINT'))
subwaydf.the_geom = subwaydf.the_geom.map(lambda string: string.strip(')'))
subwaydf.the_geom = subwaydf.the_geom.map(lambda string: string.strip(' ('))
subwaydf.the_geom = subwaydf.the_geom.map(lambda string: string.strip(','))
subwaydf.the_geom = subwaydf.the_geom.map(lambda string: string.split(' '))
for i in subwaydf.the_geom:
     i= i.reverse()


# getting unique subway stops coordinates 
subwaydf = subwaydf.drop_duplicates('NAME')
subwaydf.the_geom.dropna(inplace=True)


# loading in bus station data 

busdf = pd.read_csv('Bus_Stop_Shelter.csv')


# getting bus station coordinates 
busdf['coords'] = list(zip(busdf['LATITUDE'],busdf['LONGITUDE']))
busdf.drop_duplicates(subset = ['SHELTER_ID'],inplace =True)


# getting parks polygon data
parksdf= pd.read_csv('OpenData_ParksProperties.csv')


# cleaning geom column for polygon coords 
parksdf.the_geom=[i.strip('MULTIPOLYGON ')for i in parksdf.the_geom]
parksdf.the_geom=[i.replace(',','') for i in parksdf.the_geom]
parksdf.the_geom=[i.strip('(' and ')') for i in parksdf.the_geom]


########### only use if replace doesnt work  #################

# parksdf.the_geom=[i.strip('(') for i in parksdf.the_geom]
# parksdf.the_geom=[i.strip(')') for i in parksdf.the_geom]
# parksdf.the_geom=[i.strip('))') for i in parksdf.the_geom]
# parksdf.the_geom=[i.strip(')))') for i in parksdf.the_geom]

###################################################################

parksdf.the_geom=[i.replace(')','') for i in parksdf.the_geom]
parksdf.the_geom=[i.replace('(','') for i in parksdf.the_geom]

parksdf.the_geom=[i.split(' ') for i in parksdf.the_geom]

def get_coords(x):
    longs = []
    lats = []
    for i in range(0, len(x)):
        if i % 2:
            lats.append(float(x[i]))
        else :
            longs.append(float(x[i]))

    return list(zip(lats,longs))


parksdf.the_geom = parksdf.the_geom.apply(lambda x: get_coords(x))

# creating polygon list with shapely Polygon function
parkspolys = []
for i in parksdf.the_geom: 
    parkspolys.append(Polygon(i))