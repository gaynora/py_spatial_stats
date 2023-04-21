# -*- coding: utf-8 -*-
"""
append files from multiple in a folder
csv and excel versions
"""

import pandas as pd
import numpy as np
import os


source_file_path = r'inputs' # file path for where the file is saved
output_file_path = r'output' # file path for where the output is to be saved

aggregated = pd.DataFrame() # creates new dataframe to add all appended files into

#CSV FILES
###### loops through all entries in the file directory
for entry in os.listdir(source_file_path): 
    df=pd.read_csv(source_file_path +"\\"+ entry, usecols = ['columna', 'columnb', 'columnc']) #reads file from file path and columns

# Append to the df
    aggregated = aggregated.append (df, ignore_index=True) # appends the df to the overall df, and creates new uniue index

# output appended dataframe to new excel file
aggregated.to_csv(output_file_path + "\\" + 'appended.csv') # writes file to folder



#EXCEL FILES
###### loops through all entries in the file directory
for entry in os.listdir(source_file_path): 
    df=pd.read_excel(source_file_path +"\\"+ entry, sheet_name = 'Sheet1',usecols = 'A:C') #reads file from file path, tab and columns

# Append to the df
    aggregated = aggregated.append (df, ignore_index=True) # appends the df to the overall df, and creates new uniue index

# output appended dataframe to new excel file
aggregated.to_excel(output_file_path + "\\" + 'appended.xlsx', merge_cells = False) # writes file to folder



#SPATIAL VECTOR FILES
###### loops through all entries in the file directory
aggregated = gpd.GeoDataFrame() # creates new dataframe to add all appended files into

for entry in os.listdir(source_file_path): 
    df=gpd.read_file(source_file_path +"\\"+ entry, usecols = ['columna', 'columnb', 'columnc']) #reads file from file path and columns

# Append to the df
    aggregated = aggregated.append (df, ignore_index=True) # appends the df to the overall df, and creates new uniue index

# output appended dataframe to new spatial vector file
#aggregated.to_file(output_file_path + "\\" + 'appended.shp) # writes shapefile file to folder # writes shapefile to folder
#aggregated.to_file(output_file_path + "\\" + 'appended.geojson', driver='GeoJSON') # writes geojson file to folder
aggregated.to_file(output_file_path + "\\" + "appended.gpkg", driver="GPKG") # writes geopackage file to folder

print('Done')
