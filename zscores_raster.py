'''
python script to calculate z scores for a raster
'''

import gdal, ogr, osr, os
import numpy

#define raster file on which to calculate z scores
in_raster = gdal.Open('cand_suit2.tif')

#convert raster to array
def toarray(rasterfile):
    #raster = gdal.Open(rasterfile)
    band = rasterfile.GetRasterBand(1)
    array = band.ReadAsArray()
    array.astype(numpy.float) #use floating point to cope with decimals
    array[array <-9998] = numpy.nan    #need to change nondata values set as -9999 in gdal rasterize to NaN
    return array

array1 = toarray(in_raster) 


#calculate zscores on array
def zscore(suitabilityarray):
    mean = numpy.mean(suitabilityarray) #calculate mean
    stdev = numpy.std(suitabilityarray) #calculate standard deviation
    zscore_array = (suitabilityarray-mean)/stdev #calculate the zscores
    return zscore_array

zscore_array = zscore(array1)



#convert array to raster and save as new file
def arraytotif(inarray):
    geotransform = in_raster.GetGeoTransform() #use output parameters from area of interest mask, which will return 6 parameters including the upper left coordinates, pixel size and rotation
    ncols = array1.shape[1] #return the number of columns and rows in the array
    nrows = array1.shape[0]
    output_raster = gdal.GetDriverByName('GTiff').Create('zscores.tif',ncols, nrows, 1 ,gdal.GDT_Float32)  # create and open the raster file
    output_raster.SetGeoTransform(geotransform)  # Specify where it should be placed in space
    srs = osr.SpatialReference()                 # Establish its coordinate encoding
    srs.ImportFromEPSG(27700)                     # This one specifies British National Grid
    output_raster.SetProjection( srs.ExportToWkt() )   # Exports the coordinate system to the file
    output_raster.GetRasterBand(1).WriteArray(inarray)   # Writes array to the raster
    output_raster.FlushCache()

arraytotif(zscore_array)
