# -*- coding: utf-8 -*-
"""
Boilerplate code to create Leaflet map using Folium Python wrapper, OS Maps API Web Map Tile Service 
and some open data from a Web Feature Service

@author: G
"""

import folium
import requests
import geopandas as gpd
import matplotlib.pyplot as plt

# Define  OS MAPS API Web Map Tile Service
wmts_path = 'https://api.os.uk/maps/raster/v1/wmts?key=cf29UaahD1kovSGU2x3wyFwW09bizUGK'

# OS Maps API (WMTS) endpoint path
wmts_endpoint = 'https://api.os.uk/maps/raster/v1/wmts?'

# Define WMTS parameters 
key = 'cf29UaahD1kovSGU2x3wyFwW09bizUGK'
service = 'wmts'
request = 'GetTile'
version = '2.0.0'
style = 'default'
# Light style base map in Web Mercator projection (EPSG:3857)
layer = 'Light_3857'
tileMatrixSet = 'EPSG:3857'
tileMatrix = 'EPSG:3857:{z}'
tileRow = '{y}'
tileCol ='{x}'

# Represent WMTS parameters in a dictionary
params_wmts = {'key':key, 
              'service':service, 
              'request':request,
              'version':version,
              'style':style,
              'layer':layer,
              'tileMatrixSet':tileMatrixSet,
              'tileMatrix':tileMatrix,
              'tileRow':tileRow,
              'tileCol':tileCol}

# Construct WMTS API path
wmts_path = wmts_endpoint + \
           ('key={key}&'
            'service={service}&'
            'request={request}&'
            'version={version}&'
            'style={style}&'
            'layer={layer}&'
            'tileMatrixSet={tileMatrixSet}&'
            'tileMatrix={tileMatrix}&'
            'tileRow={tileRow}&'
            'tileCol={tileCol}').format(**params_wmts)

print('=> Constructed OS Maps API URL: {}'.format(wmts_path))

# Folium handles GeoDataFrames or JSON files as input for the interactive map
# Create a Map instance
m = folium.Map(location=[54.298093, -2.086382], zoom_start=6, control_scale=True, tiles=wmts_path, attr='Contains OS Crown Copyright')



# esri rest service url buit to return all as JSON - example of MSOA centroids here from ONS
url_final = r'https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/MSOA_Dec_2011_PWC_in_England_and_Wales_2022/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'

# either the full url is already built / known and this can be directly passed to response.get
# or the full url can be built out in python by parsing and encoding with parameters first

# define the parameters - if ESRI REST see - https://developers.arcgis.com/rest/users-groups-and-items/common-parameters.htm
params = {
    #required to build a geojson response
    'f': 'geojson', # format - JSON, PJSON, geoJSON
    'outFields': '*',  # return all fields
    'where':'1=1', # 1=1 (return all features)
    # optional
    'returnGeometry': 'true',
    # extent=<xmin>, <ymin>, <xmax>, <ymax> # bounding box to retrieve items within
    # spatialReference=GCS_North_American_1983, # CRS of item in WKID
            
}

# encode the url - if needed
#url_final = url_base + urllib.parse.urlencode(params) # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode
#print(url_final)

# query the server
response = requests.get(url=url_final)

# convert the response to text so geopandas can read it
data = response.text

# pass into a geodataframe
gdf_points = gpd.read_file(data)

# Obtain x and y coordinates of centroid point geometry
x = gdf_points.geometry.x
y = gdf_points.geometry.y

# Obtain bounds of geometry
bounds = gdf_points['geometry'][0].bounds

# Define a OGC WFS filter compliant bounding box for the geometry
# bottom-left x, bottom-left y, top-right x, top-right y
bbox = str(bounds[0]) + ',' + str(bounds[1]) + ',' + str(bounds[2]) + ',' + str(bounds[3])

# Plot points - matplotlib for test
ax = gdf_points.plot(color='#ff1f5b')
ax.axis('off')# Turn plot axis off

print('=> Transformed ONS WFS GeoJSON payload into a GeoDataFrame')

# Add points to map and save
folium.GeoJson(gdf_points).add_to(m)
#gdf_points.add_to(m)
output_map = "base_map.html"
m.save(output_map)


# upload html to webserver and share URL

