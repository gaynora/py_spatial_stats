# -*- coding: utf-8 -*-
"""
Changes to common mistakes in postcode formats.

Unit postcodes should match:
6-8 characters in total (variable)
Have one single space between 'outward' and 'inward' code: 
    outward code comes first between 2 and 4 chars
    inward code comes second exactly 3 chars long
Valid formats:
    AA9A 9AA
    A9A 9AA
    A9 9AA
    A99 9AA
    AA9 9AA
    AA99 9AA
Specific errors to check for and replace:
    enforce a single space between outward and inward codes (this may mean adding a space, or removing spaces)
    O instead of zero / 0 at start of outward code
    zero / 0 instead of O at start of inward code
    1 instead of I or L at start of inward code
    1 instead of I or L in numeic position of outward code
    5 instead of S at start of inward code
    S instead of 5 in numeric position of outward code
    8 instead B at start of inward code
    B instead of 8 in numeric position of outward code

As all formats end with 9AA, the first part of a postcode can easily be extracted by ignoring the last three characters.

Ref: https://webarchive.nationalarchives.gov.uk/ukgwa/20101126012154/http://www.cabinetoffice.gov.uk/govtalk/schemasstandards/e-gif/datastandards/address/postcode.aspx
"""

import pandas
import re

# import postcode data from csv
df = pandas.read_csv('postcode_file.csv')
'''
# IF USING A SERIES RATHER THAN DATAFRAME
#convert dataframe column with location data to series
postcode_series = df.iloc[:,0] 
print(postcode_series)
print('Total records:   ', len(df))

# count of valid format records
matches = postcode_series.str.contains('^[A-Z]{1,2}[0-9][A-Z0-9]?[\s][0-9][A-Z]{2}$')
sum_true = sum(matches) 
print('Count of series matches:   ', sum_true)
'''
# count of valid format records
df_matches = df[df['Postcodes'].str.match('^[A-Z]{1,2}[0-9][A-Z0-9]?[\s][0-9][A-Z]{2}$')]
print('Count valid format postcodes:   ', len(df_matches))
print('Percent valid format postcodes:   ', len(df_matches)/len(df)* 100)

# REPLACE ERRORS
#convert all to uppercase first
df['Postcodes_edited'] = df['Postcodes'].str.upper()
df.to_csv('first_.csv')
#where there is no whitespace in the postcode, add one before the last 3 chars
# this will enforce a space in all records
df['Postcodes_edited'] = df['Postcodes_edited'].str[:-3] + " " + df['Postcodes'].str[-3:]

# then remove extras afterwards - including any accidental entries with 2 or more spaces
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'[\s]{2,}', r' ', regex=True)

# O instead of zero / 0 at start of outward code 
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'^[0]', r'O', regex=True)

# zero / 0 instead of O at start of inward code
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'([O]{1})([A-Z]{2}$)', r'0\2', regex=True) 

# 1 instead of I, i, l or l at start of inward code
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'([ILil]{1})([A-Z]{2}$)', r'1\2', regex=True)

# 1 instead of I, i, l or L in numeic position of outward code
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'^(.{1})[ILil]', r'\g<1>1', regex=True)
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'^(.{2})[ILil]', r'\g<1>1',  regex=True)
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'^(.{3})[ILil]', r'\g<1>1',  regex=True)

# 5 instead of S at start of inward code
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'([S]{1})([A-Z]{2}$)', r'5\2', regex=True)

# 5 instead of S in numeric position of outward code
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'^(.{1})[S]', r'\g<1>5', regex=True)
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'^(.{2})[S]', r'\g<1>5',  regex=True)
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'^(.{3})[S]', r'\g<1>5',  regex=True)

# 8 instead B at start of inward code
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'([B]{1})([A-Z]{2}$)', r'8\2', regex=True)

# 8 instead of B in numeric position of outward code - this could be position 2,3 or 4 (index 1,2 or 3)
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'^(.{1})[B]', r'\g<1>8', regex=True)
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'^(.{2})[B]', r'\g<1>8',  regex=True)
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'^(.{3})[B]', r'\g<1>8',  regex=True)

print(df)
df.to_csv('postcodes_edited.csv')
