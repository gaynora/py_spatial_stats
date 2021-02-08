'''
Geocodes a set of UK records by their full unit postcode (the geographic centre of around 15 contiguous addresses). 

Uses the Office for National Statistics Postcode Directory (ONSPD) to join both projected X,Y coordinates (in British National Grid projection) and geographic long, lat coordinates (in WGS84 projection) to records where there is a valid unit postcode in the record.

Typos in records are common - most general sources of data record the unit postcode with one space between the postcode distrct and sector parts of the code, and therefore the 'pcds' field in the ONSPD table is used for the join.

'''

import numpy 
import pandas 


# import the records to be geocoded defined as a pandas dataframe
left_csv = pandas.read_csv('gctest.csv')

# import the ONSPD records with coordinate information to join as a pandas dataframe
postcode_csv = pandas.read_csv('onspd_recs.csv')

# join the tables
geocoded = left_csv.merge(postcode_csv, left_on='postcode', right_on='pcds', how='left') # the left table postcode column name may need to be changed here

# drop the fields the are not needed from the onspd table - these mostly relate to the statistical and admin area unit in which the postcode centroid falls
limited_df = geocoded.drop(['pcd', 'pcd2', 'dointr', 'doterm', 'oscty', 'ced', 'oslaua', 'osward', 'parish', 'usertype', 'osgrdind', 'oshlthau', 'nhser', 'ctry', 'rgn', 'streg', 'pcon', 'eer', 'teclec', 'ttwa', 'pct', 'nuts', 'statsward', 'oa01', 'casward', 'park', 'lsoa01', 'msoa01', 'ur01ind', 'oac01', 'oa11', 'lsoa11', 'msoa11', 'wz11', 'ccg', 'bua11', 'buasd11', 'ru11ind', 'oac11', 'lep1', 'lep2', 'pfa', 'imd', 'calncv', 'stp'], axis = 1) 

# export the table
limited_df.to_csv('geocoded.csv', index = True)
