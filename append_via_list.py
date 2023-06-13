# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:18:39 2023

@author: gaynor.astbury
"""

import pandas

table1_df = pandas.read_csv('table1.csv') # keep adding to this one and use as global variable?
table2_df = pandas.read_csv('table2.csv')
table3_df = pandas.read_csv('table3.csv')

start_df = pandas.DataFrame(columns=['Columna', 'Columnb', 'Columnc'])
dflist = [table1_df, table2_df, table3_df]

def append_list(x):
    for _ in dflist: #this would be a list of gdfs?
        x = start_df.append(x)
    return x

result = append_list(dflist)
result.to_csv('result.csv')
