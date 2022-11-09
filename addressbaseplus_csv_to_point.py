# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 11:49:28 2022
@author: gaynor.astbury
Python file to build spatial vector points datasets for Addressbase Plus, from csv downloads via the OS Data Hub in 
the format available in July 2022.
The  OS Data Hub can be accessed at https://osdatahub.os.uk/ and requires a user profile and set of credentials. 
The Addressbase Plus data download is available as part of the Public Sector Geosptial Agreement, and so beign attached 
to a government organisation is required.
"""
import pandas
import geopandas

 # Read main file from csv - Addressbase Plus downloads can be accessed in 5km tiles from https://osdatahub.os.uk/downloads/premium/ABFLDL
 # and add headers - header files are not provided with the download - these can be accessed seperately from https://www.ordnancesurvey.co.uk/business-government/tools-support/addressbase-plus-support
abplus_df = pandas.read_csv('NS6050_adressbase_plus_202207.csv', low_memory=False,  names=["UPRN", "UDPRN", "CHANGE_TYPE", "STATE", "STATE_DATE", "CLASS", "PARENT_UPRN", "X_COORDINATE", "Y_COORDINATE", "LATITUDE", "LONGITUDE", "RPC", "LOCAL_CUSTODIAN_CODE", "COUNTRY", "LA_START_DATE", "LAST_UPDATE_DATE", "ENTRY_DATE", "RM_ORGANISATION_NAME", "LA_ORGANISATION", "DEPARTMENT_NAME", "LEGAL_NAME", "SUB_BUILDING_NAME", "BUILDING_NAME", "BUILDING_NUMBER", "SAO_START_NUMBER", "SAO_START_SUFFIX", "SAO_END_NUMBER", "SAO_END_SUFFIX", "SAO_TEXT", "ALT_LANGUAGE_SAO_TEXT", "PAO_START_NUMBER", "PAO_START_SUFFIX", "PAO_END_NUMBER", "PAO_END_SUFFIX", "PAO_TEXT", "ALT_LANGUAGE_PAO_TEXT", "USRN", "USRN_MATCH_INDICATOR", "AREA_NAME", "LEVEL", "OFFICIAL_FLAG", "OS_ADDRESS_TOID", "OS_ADDRESS_TOID_VERSION", "OS_ROADLINK_TOID", "OS_ROADLINK_TOID_VERSION", "OS_TOPO_TOID", "OS_TOPO_TOID_VERSION", "VOA_CT_RECORD", "VOA_NDR_RECORD", "STREET_DESCRIPTION", "ALT_LANGUAGE_STREET_DESCRIPTOR", "DEPENDENT_THOROUGHFARE", "THOROUGHFARE", "WELSH_DEPENDENT_THOROUGHFARE", "WELSH_THOROUGHFARE", "DOUBLE_DEPENDENT_LOCALITY", "DEPENDENT_LOCALITY", "LOCALITY", "WELSH_DEPENDENT_LOCALITY", "WELSH_DOUBLE_DEPENDENT_LOCALITY", "TOWN_NAME", "ADMINISTRATIVE_AREA", "POST_TOWN", "WELSH_POST_TOWN", "POSTCODE", "POSTCODE_LOCATOR", "POSTCODE_TYPE", "DELIVERY_POINT_SUFFIX", "ADDRESSBASE_POSTAL", "PO_BOX_NUMBER", "WARD_CODE", "PARISH_CODE", "RM_START_DATE", "MULTI_OCC_COUNT", "VOA_NDR_P_DESC_CODE", "VOA_NDR_SCAT_CODE", "ALT_LANGUAGE" ]) # Read main file from csv - Addressbase Plus downloads can be accessed in 5km tiles from https://osdatahub.os.uk/downloads/premium/ABFLDL

# create geodataframe by using coodinate fields in the input dataset 
abplus_gdf = geopandas.GeoDataFrame(abplus_df, geometry=geopandas.points_from_xy(abplus_df.X_COORDINATE, abplus_df.Y_COORDINATE)) 

# set crs to BNG / EPSG 27700 if using X_COORDINATE / Y_COORDINATE fields, or European Terrestrial Reference System 89 (ETRS89) EPSG 4258 if using LATITUDE / LONGITUDE fields - method available from geopandas v0.10
# abplus_gdf = abplus_gdf.set_crs(27700, allow_override=True)

abplus_gdf.to_file('NS6050_adressbase_plus_202207.shp')# export to spatial vector file