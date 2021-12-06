# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 2021

@author: gaynora

Point in polygon aggregation calculating the mean of a set of point values within those polygons, using pandas and geopandas

Python3 script
"""

import pandas
import geopandas

noquals = geopandas.read_file('points.shp') #input points to a geodataframe
walkrail = geopandas.read_file('polygons.shp') #input polygons to a geodataframe

join_left_df = geopandas.sjoin(noquals, walkrail, how='left', op='intersects') # find and join polygon attributes to points using spatial join
mean_df = join_left_df.groupby(['IDtogroupby'])['columnvalue'].sum().reset_index() # use pandas to calculate the average with a groupby
merged = polygons.merge(mean_df, on='IDtogroupby') # join the resulting averages back to the original polygons
merged.to_file('final_result.shp') # export the results as a polygon file if needed
print(mean_df) # display the mean values if needed