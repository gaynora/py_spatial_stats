# -*- coding: utf-8 -*-
"""
Gaussian KDE using scipy
Imports coordinate locations from vector points file 
Uses optional weights, scalar bandwidth can be changed, and grid resolution via the array / meshgrid dimensions
Exports gridded results to Geotiff using GDAL

Python 3 script
"""

from scipy import stats
from shapely.geometry import Point
import geopandas
import numpy as np
from osgeo import gdal
from osgeo import osr
import pandas as pd

#open input point vector file, define the relevant field for weighting the KDE, get coordinates from geometry into 1D arrays
oas = geopandas.read_file('ew_msoa_centroids_median_age_2021_bng.shp')
x_df = oas.geometry.x #x coordinate from geometry into dataframe
x_matrix = x_df.values #then into matrix format
x = x_matrix.ravel() #then flatten matrix to 1D array
y_df = oas.geometry.y
y_matrix = y_df.values
y = y_matrix.ravel()
weight_value = oas['Medianage'] # used to weight the KDE beyond just the point location
weight_matrix = weight_value.values
weighting = weight_matrix.ravel()
values = np.vstack([x, y]) # coordinates then need to be in 2 'vertically stacked' 1D arrays for the scipy kde method

#Min and max coordinate values as bouding box for output grid
#gdf_centroidg_bb = oas.total_bounds # alternative method using geopandas directly on gdf
xmin = x.min()
xmax = x.max()
ymin = y.min()
ymax = y.max()

#create the grid for the kernal density estimation
X2, Y2 = np.mgrid[xmin:xmax:100J, ymin:ymax:100J]#, #sparse=True) #creates a 'meshgrid' for the results - cell sizes are 100j 'step sizes' or num of intervals which make the cell sizes vary, in each direction
#X2, Y2 = np.mgrid[0:660000:6600, 0:1230000:12300] #osgb bounds with 1km intervals
#THIS IS STILL NOT PRODUCING 1KM CELL SIZES AND 6600 cols rather than 100 cols

positions = np.vstack([X2.ravel(), Y2.ravel()]) # the flattened grid (into 2 1-D arrays using 'ravel')

# method for calculating the actual gaussian kde, takes 3 arguments - the coordinates, the bandwidth (can be 'silverman' for automatic bandwidth detection), and any weighting if it exists
kernel = stats.gaussian_kde(values, 0.1, weighting)
#reshape the array for the KDE back into the grid shape (T = transpose)
l = np.reshape(kernel(positions).T, X2.shape) 
z = np.rot90(l, 1)

#plot the map as a graphic 
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.imshow( z, cmap=plt.cm.gist_earth_r,
           extent=[xmin, xmax, ymin, ymax])
ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
plt.show()
#an alternative using geoplot and output from z would be better, plus use EW outline and cities

#clip z output array based on input boundary before exporting

#Setup the output raster metadata
#nrows, ncols = np.shape(z)
nrows = len(z)
ncols = len(z[0])
print(ncols) #not sure this number of columns rows is correct, it shouldn't be 100 - that is the cell or jump size

xres = (xmax-xmin)/float(ncols) # this will save hard-coding the cell sizes twice, and will calculate the cell size based on what is defined above
yres = (ymax-ymin)/float(nrows)

geotransform = (xmin,xres,0,ymax,0, -yres) # arguments taken = x-coordinate of the upper-left corner of the upper-left pixel.
                                            # w-e pixel resolution / pixel width
                                            # row rotation (typically zero)
                                            # y-coordinate of the upper-left corner of the upper-left pixel.
                                            # column rotation (typically zero).
                                            # n-s pixel resolution / pixel height (negative value for a north-up image)
#Export kernel density to geotiff

output_raster = gdal.GetDriverByName('GTiff').Create('output_kde13.tif',ncols, nrows, 1 ,gdal.GDT_Float32) # arguments passed - filename, xsize, ysize, number of bands, band type
output_raster.SetGeoTransform(geotransform) # from GDAL to convert from map to pixel coordinates and back
srs = osr.SpatialReference()
srs.ImportFromEPSG(27700) # change EPSG here to whatever CRS is needed
output_raster.SetProjection( srs.ExportToWkt() ) # applies the CRS / SRS as defined above to the geotiff
output_raster.GetRasterBand(1).WriteArray(z) # write the values calculated in the KDE to band 1 of the output raster
output_raster.FlushCache()
