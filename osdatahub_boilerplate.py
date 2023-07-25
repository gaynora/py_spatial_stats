# -*- coding: utf-8 -*-
"""
osdatahub v1 python boilerplate code
for OS Features API aownloads API

Features API:
My WFS API Endpoint address
https://api.os.uk/features/v1/wfs?key=cf29UaahD1kovSGU2x3wyFwW09bizUGK
https://osdatahub.readthedocs.io/en/latest/FeaturesAPI.html
https://labs.os.uk/prototyping/data-hub-explorer/
https://github.com/OrdnanceSurvey/osdatahub/blob/master/Examples/Plotting%20API%20Results%20-%20GeoPandas%2C%20Matplotlib%20and%20Contextily.ipynb

https://github.com/OrdnanceSurvey/osdatahub#downloads-api
"""

from osdatahub import FeaturesAPI, Extent
#from osdatahub import DataPackageDownload # for premium data orders
from osdatahub import OpenDataDownload # for open data downloads
import geopandas

# QUERY FROM FEATURES API DIRECTLY

key = "cf29UaahD1kovSGU2x3wyFwW09bizUGK" #(358190, 178443, 364262, 183927)
bbox = (0, 0, 999999, 999999) # change to area of interest bbox: left min x, bottom min y, right max x, top max y
extent = Extent.from_bbox(bbox, "EPSG:27700") # for full gb = 0, 0, 999999, 999999

product = "Zoomstack_Foreshore" # Open data categories: Zoomstack_LocalBuildings, Zoomstack_DistrictBuildings, Zoomstack_Foreshore, Zoomstack_Waterlines, Zoomstack_Surfacewater, Zoomstack_Contours, Zoomstack_Greenspace, Zoomstack_NationalParks, Zoomstack_Woodland, Zoomstack_Sites, Zoomstack_UrbanAreas, Zoomstack_Airports, OpenUSRN_USRN, Zoomstack_RoadsLocal, Zoomstack_RoadsNational, Zoomstack_RoadsRegional, Zoomstack_Boundaries, Zoomstack_Names, Zoomstack_Rail, Zoomstack_RailwayStations, Zoomstack_ETL, OpenUPRN_Address, OpenTOID_HighwaysNetwork, OpenTOID_SitesLayer, OpenTOID_TopographyLayer 
features = FeaturesAPI(key, product, extent)
results = features.query(limit=100000) #The API results are in GeoJSON format - increase the limit of features returned if needed
results_gdf = geopandas.GeoDataFrame.from_features(results['features'], crs="EPSG:27700") # use geopandas to convert the geoJSON into a geoDataframe if needed
results_gdf.to_file('zoomstackforeshore_gdf.shp') # and export the file if needed

# DOWNLOAD ENTIRE DATA FILE USING DOWNLOADS API
# for premium data packages this only works if you have first 'ordered' the data on the OS Datahub website
print(OpenDataDownload.all_products()) # to list what is available
'''
'250kScaleColourRaster', 'BoundaryLine', 'BuiltUpAreas', 'CodePointOpen', 'GBOverviewMaps', 'LIDS','MiniScale', 'OpenGreenspace',  'OpenMapLocal', 'OpenNames',  'OpenRivers',  'OpenRoads',   'OpenTOID', 'OpenUPRN', 'OpenUSRN',  'OpenZoomstack', 'Terrain50', 'VectorMapDistrict', 
'''
greenspace = OpenDataDownload("OpenGreenspace") # select the dataset of interest
print(greenspace.product_list()) # to list the specific products available to download
greenspace.download(file_name='opgrsp_essh_st.zip') # download a chosen specific dataset