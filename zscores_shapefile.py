'''
create zscores on the values in one column of a shapefile attribute table, and store in a new column

change filenames and paths as literals if needed

python 3 script
'''

import geopandas
import pandas

#import the shapefile
features = geopandas.read_file('polygons.shp')

#calculate the mean of all data points
mean = features['KS10100101'].mean()
#calculate the standard deviation of all data points
stdev = features['KS10100101'].std()
#creates new field for storing the zscore calculation and calculate the zscores
features['zscores'] = (features['KS10100101']-mean)/stdev 

#export these as another shapefile and check
features.to_file('added.shp')
