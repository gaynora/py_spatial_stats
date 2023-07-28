# -*- coding: utf-8 -*-
"""
Query of ESRI REST API WFS boilerplate

@author: G
"""

import requests
import urllib.parse
import geopandas as gpd

# base url
#url_base = r'https://services.arcgis.com/JJzESW51TqeY9uat/ArcGIS/rest/services/Special_Areas_of_Conservation_England/FeatureServer/0/query?'
# same esri rest service url buit to return all as JSON
url_final = r'https://services.arcgis.com/JJzESW51TqeY9uat/arcgis/rest/services/Special_Areas_of_Conservation_England/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'

# either the full url is already built / known and this can be directly passed to response.get
'''
# or the full url can be built out in python by parsing and encoding with parameters first

# define the parameters - https://developers.arcgis.com/rest/users-groups-and-items/common-parameters.htm
params = {
    #required to build a geojson response
    'f': 'geojson', # format - JSON, PJSON, geoJSON
    'outFields': '*',  # return all fields
    'where':'1=1', # 1=1 (return all features)
    # optional
    #'returnGeometry': 'true',
    # extent=<xmin>, <ymin>, <xmax>, <ymax> # bounding box to retrieve items within
    # spatialReference=GCS_North_American_1983, # CRS of item in WKID
            
}


# encode the url - if needed
#url_final = url_base + urllib.parse.urlencode(params) # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode
#print(url_final)
'''
# query the server
response = requests.get(url=url_final)

# convert the response to text so geopandas can read it
data = response.text

# pass into a geodataframe
gdf_temp = gpd.read_file(data)
# and export to vector file if needed
gdf_temp.to_file('output.shp')