# -*- coding: utf-8 -*-
"""
@author: gaynor.astbury
"""

import pandas

#import the csvs
first_csv= pandas.read_csv('csv1.csv') #change filenames and paths as literals if needed
second_csv = pandas.read_csv('csv2.csv')
third_csv = pandas.read_csv('csv3.csv')
# multiple csvs may be added

csv_list = [second_csv, third_csv]

# the for loop sits inside a function so that it calls itself
# assign the result of the append function to the variable that you use as 
# the argument to the append function.


def do_append(x):
    for _ in csv_list:
        z = x.append(csv_list, ignore_index=True)
    return z

# start with an initial csv file as the argument to the do_append() function
output = do_append(first_csv)
output.to_csv('output.csv')