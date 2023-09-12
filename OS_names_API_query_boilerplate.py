# -*- coding: utf-8 -*-
"""
Get requests for the OS Names REST API at 2023.
Search for names of areas, cities, roads, postcodes and named woodlands and forests. 
Themes include populated places e.g. cities / transport network e.g. bus stations / landform e.g. coastal headlands / hydrography e.g. bays / landcover e.g. woodland and forests / other e.g. chemical works / 
Authentication is required for this API, with keys available from https://osdatahub.os.uk accounts
Default format response is JSON.
author: @gaynora
"""

import requests
import pandas
import json
from pandas.io.json import json_normalize


# USING THE 'FIND' OPERATION - INTENDED TO BE A FREE-TEXT FUZZY SEARCH
params = {
          "key" : "cf29UaahD1kovSGU2x3wyFwW09bizUGK", # required API key
          "query" : "Dursley", # required freetext search criteria
          "maxresults" : "100", # optional. The maximum number of results to return. Default: 100.
          "bounds": "372850,195921,377319,201009", # optional. Biases the results to a certain area. The 'bounds' parameter must be a pair of comma separated coordinate sets in British National Grid projection with an accuracy of 2 decimal places or less e.g. 400000,200000,400300,200700
          #"fq": "Bus_Station", # optional string. Filters the results by bounding box or local_type. The bounding box is a British National Grid bounding box in the form: XMIN,YMIN,XMAX,YMAX e.g. &fq=BBOX:414000,114000,414100,114100.
          "format": "JSON" # optional. 'JSON', 'XML' but the below code parses JSON
          #"offset": "1", # optional integer to offset the list of returned results by this amount.
}

response = requests.get('https://api.os.uk/search/names/v1/find', params=params) # makes the get request

json_data = json.loads(response.text) # assigns the results as JSON to a variable
json_data2 = pandas.json_normalize(json_data, record_path=['results']) # returns only the 'results' part of the API response, and 'flattens' the JSON data structure into a flat dataframe
print(json_data2)

df = pandas.DataFrame(json_data2) # loads the flattened data into a dataframe variable

df.to_csv('results_find.csv') # exports the results and writes as a file to disk if needed

#USING THE NEAREST OPERATION - RETURNS A SINGLE CLOSEST RECORD TO A GIVEN SET OF COORDINATES
params = {
          "key" : "cf29UaahD1kovSGU2x3wyFwW09bizUGK", # required API key
          "point" : "375400.21, 198700.00", # required. A set of British National Grid coordinates to which the nearest record in a straight line should be found. The precision of the coordinates is to two decimal places (i.e. 1cm accuracy).
          #"radius" : "100", # optional. 0.01 - 1000. The radius in metres to search within.The precision of the distance is to two decimal places (i.e. 1 cm accuracy). Default: 100.  
          #"fq": "Bus_Station", # optional string. Filters the results by bounding box or local_type (list available via OS technical notes). The bounding box is a British National Grid bounding box in the form: XMIN,YMIN,XMAX,YMAX e.g. &fq=BBOX:414000,114000,414100,114100.
          "format": "JSON" # optional. 'JSON', 'XML' but the below code parses JSON
}

response2 = requests.get('https://api.os.uk/search/names/v1/nearest', params=params) # makes the get request

json_data2 = json.loads(response2.text) # assigns the results as JSON to a variable
print(json_data2)

json_data3 = pandas.json_normalize(json_data2, record_path=['results']) # returns only the 'results' part of the API response, and 'flattens' the JSON data structure into a flat dataframe
print(json_data3)

df = pandas.DataFrame(json_data3) # loads the flattened data into a dataframe variable

df.to_csv('results_near.csv') # exports the results and writes as a file to disk if needed
