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
output_file_name = "appended.xlsx" # name of the input file to be read in


aggregated = pd.DataFrame() # creates new dataframe to add all appended files into

#CSV FILES
###### loops through all entries in the file directory
for entry in os.listdir(source_file_path): 
    df=pd.read_csv(source_file_path +"\\"+ entry, usecols = ['columna', 'columnb', 'columnc']) #reads file from file path and columns

# Append to the df
    aggregated = aggregated.append (df, ignore_index=True) # appends the df to the overall df, and creates new uniue index

# output appended dataframe to new excel file
aggregated.to_csv(output_file_path + "\\" + output_file_name) # writes file to folder


#EXCEL FILES
###### loops through all entries in the file directory
#for entry in os.listdir(source_file_path): 
    #df=pd.read_excel(source_file_path +"\\"+ entry, sheet_name = 'Sheet1',usecols = 'A:C') #reads file from file path, tab and columns

# Append to the df
    #aggregated = aggregated.append (df, ignore_index=True) # appends the df to the overall df, and creates new uniue index

# output appended dataframe to new excel file
#aggregated.to_excel(output_file_path + "\\" + output_file_name,merge_cells = False) # writes file to folder

print('Done')
