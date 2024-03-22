# -*- coding: utf-8 -*-
"""
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

All alpha chars to be uppercase: convert first before below checks.
Specific errors to check for and replace:
    enforce a single space between outward and inward codes (this may mean adding a space, or removing spaces)
    O instead of zero / 0 at start of outward code
    zero / 0 instead of O at start of inward code
    1 instead of I or L at start of inward code
    1 instead of I or L in numeic position of outward code

As all formats end with 9AA, the first part of a postcode can easily be extracted by 
ignoring the last three characters.

str.match() in pandas
"""

import pandas

# import QRT data from csv
df = pandas.read_csv('postcode_file.csv')
#convert dataframe column with location data to series
postcode_series = df.iloc[:,0] 
print(postcode_series)
print('Total records:   ', len(df))

# FORMAT VALIDATION COUNTS
'''
# overall count of valid format records using the series
matches = postcode_series.str.contains('^[A-Z]{1,2}[0-9][A-Z0-9]?[\s][0-9][A-Z]{2}$')
sum_true = sum(matches) 
print('Count of series matches:   ', sum_true)
'''

df_matches = df[df['Postcodes'].str.match('^[A-Z]{1,2}[0-9][A-Z0-9]?[\s][0-9][A-Z]{2}$')]
df_matches.to_csv('df_matches.csv')
print('Count valid format postcodes:   ', len(df_matches))
print('Percent valid format postcodes:   ', len(df_matches)/len(df)* 100)

# REPLACE ERRORS
#convert all to uppercase first
df['Postcodes_edited'] = df['Postcodes'].str.upper()

#where there is no whitespace in the postcode, add one before the last 3 chars
# NEEDS FIXING
for x in df['Postcodes_edited'] :   
    if " " not in x:
        x = x[:-3] + " " + x[-3:]

#df['Postcodes_edited'] = df['Postcodes'].str[:3] + " " + df['Postcodes'].str[2:]

# O instead of zero / 0 at start of outward code 
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'^[0]', r'O', regex=True)

# zero / 0 instead of O at start of inward code
# 3 FROM THE END POSITION NEEDS FIXING
df['Postcodes_edited'] = df['Postcodes_edited'].str.replace(r'.{2}$[O]', r'0', regex=True)

print(df)
df.to_csv('postcodes_edited.csv')

