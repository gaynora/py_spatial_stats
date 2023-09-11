# -*- coding: utf-8 -*-
"""
Get requests for the OS Names API at 2023.
Search for areas, cities, roads, postcodes and named woodlands and forests.
Authentication is required for this API, with keys available from https://osdatahub.os.uk accounts
Default format response is JSON.
author: @gaynora
"""

import requests
import pandas
import json
from pandas.io.json import json_normalize

# using the 'find' operation - intended to be a free-text fuzzy search
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

df.to_csv('results.csv') # exports the results and writes as a file to disk if needed
