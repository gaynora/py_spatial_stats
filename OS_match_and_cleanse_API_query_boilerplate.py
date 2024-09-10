# -*- coding: utf-8 -*-

"""
Get requests for the OS Match and Cleanse REST API at 2023.
Detailed UK address matching using Addressbase Premium and Islands. 
Each address returned is given a match score from 0 to 1.0, where 1.0 represents an EXACT match with control over the precision of the result.
Authentication is required for this API, with keys available from https://osdatahub.os.uk accounts 
A premium data subscription or membership of the PSGA is required to access data.
Default format response is JSON. All calls must be over HTTPS.
Docu on data content, query parameters and return codes - https://osdatahub.os.uk/docs/match/technicalSpecification
author: @gaynora
"""

import requests
import pandas
import json
from pandas.io.json import json_normalize

# ONE TYPE OF REQUEST = 'MATCH' IS AVAILABLE USING A FREETEXT SEARCH

params = {
          "key" : "xxx", # required API key
          "query" : "freetext here", # required freetext search criteria
          "format": "JSON", # optional. 'JSON', 'XML' but the below code parses JSON
          "maxresults" : "100", # optional. The maximum number of results to return. Default: 100.
          #"offset": "100", # optional integer offsetting the list of returned results by this amount.
          "dataset" : "LPI", # optional. 'DPA', 'LPI' / Delivery Point Address, Land and Property Identifier or both values can be sent and datasets searched. Please see notes for explanation of difference.
          #"lr": "EN", # optional language for return results EN / CY, English / Welsh.
          #"minmatch" : "0.5", # optional. 0.1 - 1.0 (inclusive - 1 being an exact match) The minimum match score a result has to have to be returned.
          #"matchprecision" : "1", # optional. '1' - '10' The decimal point position at which the match score value is to be truncated.
          #"fq" : "", # optional. 'CLASSIFICATION_CODE:[code]', 'LOGICAL_STATUS_CODE:[code]', 'COUNTRY_CODE:[code]' A filter that allows filtering of results by classification code, logical status code and/or country code, or multiple. 
          #"output_srs" : "EPSG:27700" # optional. 'BNG', 'EPSG:27700', 'WGS84', 'EPSG:4326', 'EPSG:3857', 'EPSG:4258'. The intended output spatial reference system. Default: EPSG:27700.
}

response = requests.get('https://api.os.uk/search/match/va/match', params=params) # makes the get request

json_data = json.loads(response.text) # assigns the results as JSON to a variable


json_data2 = pandas.json_normalize(json_data, record_path=['results']) # returns only the 'results' part of the API response, and 'flattens' the JSON data structure into a flat dataframe
print(json_data2)

df = pandas.DataFrame(json_data2) # loads the flattened data into a dataframe variable

df.to_csv('results_find.csv') # exports the results and writes as a file to disk if needed
