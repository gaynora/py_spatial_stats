# -*- coding: utf-8 -*-
"""
Get features from OS Features REST API within a defined bounding box
API supports max 100 records, so need to paginate through dataset
https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/technical-specification/paging
The OS Features API returns the OS Mastermap large-scale topography data
Author @gaynora
"""

import geopandas as gpd
import pandas as pd
import requests
from io import BytesIO

api_key = "API_KEY_HERE" # will need changing - requires a premium account or access to premium data
wfs_url = "https://api.os.uk/features/v1/wfs" # endpoint
layer_name = "Topography_TopographicArea"  # supported typeNames list here https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/technical-specification/getfeature
bbox = (358400, 171600, 361000, 173800)  # minx, miny, maxx, maxy default EPSG 27700 

# WFS PARAMETERS
params = {
    "service": "WFS",
    "version": "2.0.0",
    "request": "GetFeature",
    "typeNames": layer_name,
    "bbox": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
    "srsName": "EPSG:27700", # may need changing depending on what server supports
    "outputFormat": "GEOJSON",
    "key": api_key,
    "count": 100, # maximum 100 record in single request
    "limit": 100,         
    "startIndex": 0,        
    "offset":0
}

all_gdfs = [] # create empty geodataframe to store the results
start = 0
page_size = 100

# loop through 110 record requests until all features have been returned 
# within the bounding box and concatenante together
while True:
    params["startIndex"] = start
    response = requests.get(wfs_url, params=params)
    response.raise_for_status()
    gdf_page = gpd.read_file(BytesIO(response.content))
    if gdf_page.empty:
        break
    all_gdfs.append(gdf_page)
    start += page_size

gdf = gpd.GeoDataFrame(pd.concat(all_gdfs, ignore_index=True))
gdf.to_file('paginated_output2.geojson') # export the result
