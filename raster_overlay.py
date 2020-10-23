'''
create a raster overlay in python
all of the input rasters values should represent the same metric, if not these should be standardised prior to doing an overlay
'''

import gdal, ogr, osr, os
import numpy

# choose the various rasters to overlay
study_area = gdal.Open('study_area.tif') # define a study area that encompasses all of the input rasters
raster1 = gdal.Open('raster1.tif') # ideally the rasters will have the same cell size and alignments as each other
raster2 = gdal.Open('raster2.tif')


# covert rasters to arrays
def raster2array(rasterfile):
    band = rasterfile.GetRasterBand(1)
    array = band.ReadAsArray()
    array.astype(numpy.float) # use floating point to cope with decimals
    array[array <-9998] = numpy.nan    # need to change nondata values set as -9999 in gdal rasterize to NaN
    return array

var1 = raster2array(raster1)
var2 = raster2array(raster2)


# add the arrays - unweighted
overlay_array = var1 + var2 # + var3 etc
'''
# add the arrays - weighted
overlay_array = (var1*2)+(var2*3) # etc, using literals as the appropriate weights
'''

# convert the result back to a raster and save
def arraytotif(inarray):
    geotransform = study_area.GetGeoTransform() # use output parameters from the study area mask, which will return 6 parameters including the upper left coordinates, pixel size and rotation
    ncols = array1.shape[1] # return the number of columns and rows in the array
    nrows = array1.shape[0]
    output_raster = gdal.GetDriverByName('GTiff').Create('overlay.tif',ncols, nrows, 1 ,gdal.GDT_Float32)  # create and open the raster file
    output_raster.SetGeoTransform(geotransform)  # specify where it should be placed in space
    srs = osr.SpatialReference()                 # establish its coordinate encoding
    srs.ImportFromEPSG(27700)                     # this one specifies British National Grid
    output_raster.SetProjection( srs.ExportToWkt() )   # exports the coordinate system to the file
    output_raster.GetRasterBand(1).WriteArray(inarray)   # writes array to the raster
    output_raster.FlushCache()

arraytotif(overlay_array)



