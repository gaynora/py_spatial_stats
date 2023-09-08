# -*- coding: utf-8 -*-
"""
Boilerplate for spatial data vector to raster conversion, utilising geodataframes: single feature method
Currently an extra step is required to translate between GDAL and Geopandas:
    method writes geodataframe to disk as an interim step
    
Python3 script

@author: gaynora, created 2023
"""
from osgeo import gdal, ogr
import geopandas

# let's presume a geodataframe has already been created somewhere within the code
# which may have been via importing a vector file
input_poly_gdf = geopandas.read_file('test_rasterise.shp', crs="EPSG:27700")
#this geodataframe needs to be written to disk
input_poly_gdf.to_file('test_rasterise2.shp', crs="EPSG:27700")
# and imported through the gdal/ogr method to use the GDAL rasterize function and associated methods e.g. GetLayer()
input_poly = ogr.Open('test_rasterise2.shp')

output_raster = 'converted.tif'  #filename of output converted raster - define a directory if needed

# bounds are taken from the original geodataframe, using a geopandas method
x = input_poly_gdf.bounds # takes all of the bounds into a dataframe
x_min = x.iloc[0].minx # locates each bound to an individual variable
y_min = x.iloc[0].miny # assumes only one feature is present
x_max = x.iloc[0].maxx # as it locates values on the first row
y_max = x.iloc[0].maxy

#vector to raster conversion
def rasterize(vectorfile):
    pixel_size = 1000       # pixel size of new raster - can be changed via a literal for different resolutions
    NoData_value = -9999    # NoData value of new raster - check this in the input raster and change if necessary
    source_layer = vectorfile.GetLayer() 
    x_res = int((x_max - x_min) / pixel_size)+1          # create the destination data source
    y_res = int((y_max - y_min) / pixel_size)+1          # use +1 to get over the full extent and overcome offset issue
    target_ds = gdal.GetDriverByName('GTiff').Create(output_raster, x_res, y_res, 1, gdal.GDT_Float64)# this needs to be floating point for subsequent arrays created to deal with NaN nodata values
    target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
    target_ds.SetProjection(source_layer.GetSpatialRef().ExportToWkt()) # set the projection of the output raster to match the input shapefile
    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(NoData_value)
    gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[0], options =['ATTRIBUTE=id','ALL_TOUCHED=TRUE'] ) # Convert - define the correct field to use as the raster cell value. The field must be a floating point type in order for NoData values of -9999 to be assigned.
    target_ds = None # close dataset

rasterize(input_poly)
