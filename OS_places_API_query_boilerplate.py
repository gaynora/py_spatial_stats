# -*- coding: utf-8 -*-
"""
Requests for the OS Places REST API at 2023.
Contains detailed addreses including all the records of AddressBase® Premium and AddressBase® Premium – Islands and so provides all the information relating to an address or property from creation to retirement.
Can search on free text, postcode, UPRNs, closet and radius to coord, BBox, geoJSON polygon (post request).
Docu on dataset content, query parameters, call methods and return codes at https://osdatahub.os.uk/docs/places/technicalSpecification
Authentication is required for this API, with keys available from https://osdatahub.os.uk accounts
Default format response is JSON.
Python 3 script: limited methods can also be acheived through the osdatahub package, in addition to the requests package.
author: @gaynora
"""

import requests
import pandas
#import geopandas
import json
from pandas.io.json import json_normalize


# USING THE FIND OPERATION - INTENDED FOR FREE TEXT SERACHES
params = {
          "key" : "u6phAc81uEMug55KYaAj6NIhrFI2QVi7", # required API key
          "query" : "1 Horse Guards", # required freetext search criteria
          #"format" : "", # optional. 'JSON', 'XML' data type returned. Default JSON.
          "maxresults" : "50", # optional. 1 - 100. Max number of results to return.
          #"offset" : "1", # optional. Offset the list of returned results by this amount.
          "dataset" : "LPI" # optional. 'DPA', 'LPI'. The dataset to return. Multiple values can be sent, separated by a comma. Default: DPA. Please see OS technical notes for explanation of both.
          #"lr" : "", # optional. 'EN', 'CY'Language of data return. English or Welsh.
          #"minmatch" : "", # optional. 0.1 - 1.0 (inclusive) The minimum match score a result has to have to be returned.
          #"matchprecision" : "", # optional. '1' - '10'. The decimal point position at which the match score value is to be truncated.
          #"fq" : "", # optional. 'CLASSIFICATION_CODE:[code]', 'LOGICAL_STATUS_CODE:[code]', 'COUNTRY_CODE:[code]','LOCAL_CUSTODIAN_CODE:[code]' filtering of results by classification code, logical status code, country code and local custodian code.
         # "output_srs" : "" # optional. 'BNG', 'EPSG:27700', 'WGS84', 'EPSG:4326', 'EPSG:3857', 'EPSG:4258' The intended output spatial reference system. Default: EPSG:27700.
}

response_find = requests.get('https://api.os.uk/search/places/v1/find', params=params) # makes the get request

json_data_find = json.loads(response_find.text) # assigns the results as JSON to a variable

json_data_find2 = pandas.json_normalize(json_data_find, record_path=['results']) # returns only the 'results' part of the API response, and 'flattens' the JSON data structure into a flat dataframe
print(json_data_find2)

df = pandas.DataFrame(json_data_find2) # loads the flattened data into a dataframe variable

df.to_csv('results_places_find.csv') # exports the results and writes as a file to disk if needed


# USING THE POSTCODE OPERATION

params = {
          "key" : "u6phAc81uEMug55KYaAj6NIhrFI2QVi7", # required API key
          "postcode" : "SW1A 2AS", # required.  A UK style postcode.
          #"format" : "", # optional. 'JSON', 'XML' data type returned. Default JSON.
          "maxresults" : "50", # optional. 1 - 100. Max number of results to return.
          #"offset" : "1", # optional. Offset the list of returned results by this amount.
          "dataset" : "LPI" # optional. 'DPA', 'LPI'. The dataset to return. Multiple values can be sent, separated by a comma. Default: DPA. Please see OS technical notes for explanation of both.
          #"lr" : "", # optional. 'EN', 'CY'Language of data return. English or Welsh.
          #"fq" : "", # optional. 'CLASSIFICATION_CODE:[code]', 'LOGICAL_STATUS_CODE:[code]', 'COUNTRY_CODE:[code]','LOCAL_CUSTODIAN_CODE:[code]' filtering of results by classification code, logical status code, country code and local custodian code.
         # "output_srs" : "" # optional. 'BNG', 'EPSG:27700', 'WGS84', 'EPSG:4326', 'EPSG:3857', 'EPSG:4258' The intended output spatial reference system. Default: EPSG:27700.
}

response_postcode = requests.get('https://api.os.uk/search/places/v1/postcode', params=params) # makes the get request

json_data_postcode = json.loads(response_postcode.text) # assigns the results as JSON to a variable

json_data_postcode2 = pandas.json_normalize(json_data_postcode, record_path=['results']) # returns only the 'results' part of the API response, and 'flattens' the JSON data structure into a flat dataframe
print(json_data_postcode2)

df = pandas.DataFrame(json_data_postcode2) # loads the flattened data into a dataframe variable

df.to_csv('results_places_postcode.csv') # exports the results and writes as a file to disk if needed


# USING THE UPRN OPERATION

params = {
          "key" : "u6phAc81uEMug55KYaAj6NIhrFI2QVi7", # required API key
          "uprn" : "10033548201", # required.  Unique Property Reference Number
          #"format" : "", # optional. 'JSON', 'XML' data type returned. Default JSON.
          "dataset" : "LPI" # optional. 'DPA', 'LPI'. The dataset to return. Multiple values can be sent, separated by a comma. Default: DPA. Please see OS technical notes for explanation of both.
          #"lr" : "", # optional. 'EN', 'CY'Language of data return. English or Welsh.
          #"fq" : "", # optional. 'CLASSIFICATION_CODE:[code]', 'LOGICAL_STATUS_CODE:[code]', 'COUNTRY_CODE:[code]','LOCAL_CUSTODIAN_CODE:[code]' filtering of results by classification code, logical status code, country code and local custodian code.
         # "output_srs" : "" # optional. 'BNG', 'EPSG:27700', 'WGS84', 'EPSG:4326', 'EPSG:3857', 'EPSG:4258' The intended output spatial reference system. Default: EPSG:27700.
}

response_uprn = requests.get('https://api.os.uk/search/places/v1/uprn', params=params) # makes the get request

json_data_uprn = json.loads(response_uprn.text) # assigns the results as JSON to a variable

json_data_uprn2 = pandas.json_normalize(json_data_uprn, record_path=['results']) # returns only the 'results' part of the API response, and 'flattens' the JSON data structure into a flat dataframe
print(json_data_uprn2)

df = pandas.DataFrame(json_data_uprn2) # loads the flattened data into a dataframe variable

df.to_csv('results_places_uprn.csv') # exports the results and writes as a file to disk if needed


# USING THE NEAREST OPERATION

params = {
          "key" : "u6phAc81uEMug55KYaAj6NIhrFI2QVi7", # required API key
          "point" : "530047, 179748", # required.  comma-separated coordinates to which the nearest record in a straight line should be found. Max 1000 metres.
          #"radius" : "1000", # optional. 0.01 - 1000. The radius in metres to search within. Maximum is 1,000 metres. If the radius exceeds that amount then an error message will be returned (see below).
          #"format" : "", # optional. 'JSON', 'XML' data type returned. Default JSON.
          "dataset" : "LPI" # optional. 'DPA', 'LPI'. The dataset to return. Multiple values can be sent, separated by a comma. Default: DPA. Please see OS technical notes for explanation of both.
          #"lr" : "", # optional. 'EN', 'CY'Language of data return. English or Welsh.
          #"fq" : "", # optional. 'CLASSIFICATION_CODE:[code]', 'LOGICAL_STATUS_CODE:[code]', 'COUNTRY_CODE:[code]','LOCAL_CUSTODIAN_CODE:[code]' filtering of results by classification code, logical status code, country code and local custodian code.
          #"output_srs", : "" # optional. 'BNG', 'EPSG:27700', 'WGS84', 'EPSG:4326', 'EPSG:3857', 'EPSG:4258' The intended output spatial reference system. Default: EPSG:27700.
          #"srs" : "EPSG:27700" # 'BNG', 'EPSG:27700', 'WGS84', 'EPSG:4326', 'EPSG:3857', 'EPSG:4258' The spatial reference system for the input coordinate set.
}

response_nearest = requests.get('https://api.os.uk/search/places/v1/nearest', params=params) # makes the get request

json_data_nearest = json.loads(response_nearest.text) # assigns the results as JSON to a variable

json_data_nearest2 = pandas.json_normalize(json_data_nearest, record_path=['results']) # returns only the 'results' part of the API response, and 'flattens' the JSON data structure into a flat dataframe
print(json_data_nearest2)

df = pandas.DataFrame(json_data_nearest2) # loads the flattened data into a dataframe variable

df.to_csv('results_places_nearest.csv') # exports the results and writes as a file to disk if needed


# USING THE BBox OPERATION Takes two points and creates a bounding box. All addresses within this bounding box are then returned.

params = {
          "key" : "u6phAc81uEMug55KYaAj6NIhrFI2QVi7", # required API key
          "bbox" : "529940, 179711, 530307, 179905", # required.  comma-separated coordinates that specify the lower left and upper right coordinates of the bounding box.
          #"format" : "", # optional. 'JSON', 'XML' data type returned. Default JSON.
          "maxresults" : "100", # 1 - 100. The maximum number of results to return.
          #"offset" : "1", # Offset the list of returned results by this amount.
          "dataset" : "LPI" # optional. 'DPA', 'LPI'. The dataset to return. Multiple values can be sent, separated by a comma. Default: DPA. Please see OS technical notes for explanation of both.
          #"lr" : "", # optional. 'EN', 'CY'Language of data return. English or Welsh.
          #"fq" : "", # optional. 'CLASSIFICATION_CODE:[code]', 'LOGICAL_STATUS_CODE:[code]', 'COUNTRY_CODE:[code]','LOCAL_CUSTODIAN_CODE:[code]' filtering of results by classification code, logical status code, country code and local custodian code.
          #"output_srs", : "" # optional. 'BNG', 'EPSG:27700', 'WGS84', 'EPSG:4326', 'EPSG:3857', 'EPSG:4258' The intended output spatial reference system. Default: EPSG:27700.
          #"srs" : "EPSG:27700" # 'BNG', 'EPSG:27700', 'WGS84', 'EPSG:4326', 'EPSG:3857', 'EPSG:4258' The spatial reference system for the input coordinate set.
}

response_bbox = requests.get('https://api.os.uk/search/places/v1/bbox', params=params) # makes the get request

json_data_bbox = json.loads(response_bbox.text) # assigns the results as JSON to a variable

json_data_bbox2 = pandas.json_normalize(json_data_bbox, record_path=['results']) # returns only the 'results' part of the API response, and 'flattens' the JSON data structure into a flat dataframe
print(json_data_bbox2)

df = pandas.DataFrame(json_data_bbox2) # loads the flattened data into a dataframe variable

df.to_csv('results_places_bbox.csv') # exports the results and writes as a file to disk if needed


# USING THE RADIUS OPERATION Takes a pair of coordinates as the centre for a circle and returns all addresses that are intersected by it.

params = {
          "key" : "u6phAc81uEMug55KYaAj6NIhrFI2QVi7", # required API key
          "point" : "530047, 179748", # required.  One comma-separated coordinate set that specifies the coordinate to which the nearest record in a straight line should be found.  
          "radius" : "1000", # optional. 0.01 - 1000. The radius in metres to search within.
          #"format" : "", # optional. 'JSON', 'XML' data type returned. Default JSON.
          "maxresults" : "100", # 1 - 100. The maximum number of results to return.
          #"offset" : "1", # Offset the list of returned results by this amount.
          "dataset" : "LPI" # optional. 'DPA', 'LPI'. The dataset to return. Multiple values can be sent, separated by a comma. Default: DPA. Please see OS technical notes for explanation of both.
          #"lr" : "", # optional. 'EN', 'CY'Language of data return. English or Welsh.
          #"fq" : "", # optional. 'CLASSIFICATION_CODE:[code]', 'LOGICAL_STATUS_CODE:[code]', 'COUNTRY_CODE:[code]','LOCAL_CUSTODIAN_CODE:[code]' filtering of results by classification code, logical status code, country code and local custodian code.
          #"output_srs", : "" # optional. 'BNG', 'EPSG:27700', 'WGS84', 'EPSG:4326', 'EPSG:3857', 'EPSG:4258' The intended output spatial reference system. Default: EPSG:27700.
          #"srs" : "EPSG:27700" # 'BNG', 'EPSG:27700', 'WGS84', 'EPSG:4326', 'EPSG:3857', 'EPSG:4258' The spatial reference system for the input coordinate set.
}

response_radius = requests.get('https://api.os.uk/search/places/v1/radius', params=params) # makes the get request

json_data_radius = json.loads(response_radius.text) # assigns the results as JSON to a variable

json_data_radius2 = pandas.json_normalize(json_data_radius, record_path=['results']) # returns only the 'results' part of the API response, and 'flattens' the JSON data structure into a flat dataframe
print(json_data_radius2)

df = pandas.DataFrame(json_data_radius2) # loads the flattened data into a dataframe variable

df.to_csv('results_places_radius.csv') # exports the results and writes as a file to disk if needed
