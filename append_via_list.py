# -*- coding: utf-8 -*-
"""
Appends multiple dataframes from seperate input files using a loop within a function.
All input table schemas must match.
Python 3 script.

@author: gaynor.astbury
"""

import pandas

table1_df = pandas.read_csv('table1.csv') 
table2_df = pandas.read_csv('table2.csv')
table3_df = pandas.read_csv('table3.csv')

start_df = pandas.DataFrame(columns=['Columna', 'Columnb', 'Columnc']) # empty dataframe to start - schema may need editing
dflist = [table1_df, table2_df, table3_df]

def append_list(x):
    for _ in dflist: 
        x = start_df.append(x)
    return x

result = append_list(dflist)
result.to_csv('result.csv')
