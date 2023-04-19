# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 10:02:21 2022

@author: gaynor.astbury
"""

import pandas
import geopandas

polygons_gdf = geopandas.read_file('polygons.shp')

points_gdf = polygons_gdf.copy()
points_gdf['geometry'] = points_gdf['geometry'].centroid

points_gdf.to_file('points.shp')