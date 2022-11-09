# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 16:37:36 2022

@author: gaynor.astbury
"""

# -*- coding: utf-8 -*-
"""

@author: gaynor.astbury
Python file to build spatial vector points datasets from a coordinate fields
"""
import pandas
import geopandas

 # Read holding extract from the above SQL Server database and add headers 
input_df = pandas.read_csv('input.csv', encoding='iso-8859-1', low_memory=False) # or UTF8 / other encoding


# create geodataframe by using coodinate fields in the input dataset 
gdf = geopandas.GeoDataFrame(input_df, geometry=geopandas.points_from_xy(input_df.OSGBGridRefEast,input_df.OSGBGridRefNorth)) 

# set crs to EPSG 27700 if using coordinates for properties located in Great Britain, 
# or EPSG 29902 if using coordinates located in Northern Ireland records, 
# or EPSG 4326 if using fields coordinates globally - method only available from geopandas v0.10
#gdf = gdff.set_crs(27700, allow_override=True)

# export to spatial vector file
gdf.to_file('output_points.shp')
