# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:39:03 2023

@author: G
"""

from owslib.wfs import WebFeatureService
import geopandas as gpd
from requests import Request


# READ WFS CAPABILITIES AND METADATA
url = "https://ogc.bgs.ac.uk/digmap625k_gsml_insp_gs/wfs" # URL for WFS backend - to be edited 
wfs = WebFeatureService(url=url) # Initialize
print(wfs.identification.title) # Service provider 
print(wfs.version) # Get WFS version
#print([operation.name for operation in wfs.operations]) # Available methods
#print(list(wfs.contents)) # Available data layers
#for layer, meta in wfs.items(): # Print all metadata of all layers
#    print(meta.__dict__)
    
# READ THE DATA INTO GEODATAFRAME:
layer_name = list(wfs.contents)[-1] # Fetch the last available layer (as an example) 
params = dict(service='WFS', version="1.0.0", request='GetFeature', # Specify the parameters for fetching the data
      typeName=layer_name, outputFormat='json', count=100, startIndex=0) # Count: amount of rows to return, startIndex: offset to start returning rows

wfs_request_url = Request('GET', url, params=params).prepare().url # Parse the URL with parameters

data = gpd.read_file(wfs_request_url) # Read data from URL
data.to_file('output.shp')



#FUNCTIONAL APPROACH
def get_wfs(url):
   
    wfs = WebFeatureService(url) # initialise    
    layer_name = list(wfs.contents)[-1] # Fetch the last available layer (as an example)    
    params = dict(service='WFS', version="1.0.0", request='GetFeature', typeName=layer_name, outputFormat='json', count=100, startIndex=0) # Specify the parameters for fetching the data Count: amount of rows to return, startIndex: offset to start returning rows    
    wfs_request_url = Request('GET', url, params=params).prepare().url # Parse the URL with parameters    
    wfs_gdf = gpd.read_file(wfs_request_url) # return wfs_request_url
    return wfs_gdf
    
url2 = "https://ogc.bgs.ac.uk/digmap625k_gsml_insp_gs/wfs" # example - can be edited
x = get_wfs(url2) # assign to geodataframe
x.to_file('output2.shp') # export to vector


