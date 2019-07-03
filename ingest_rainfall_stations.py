#!/usr/bin/env python
# coding: utf-8
import requests
import json
import urllib
import  urllib.parse
import pandas as pd
from subprocess import call
from pyproj import Proj, transform
from requests.auth import HTTPBasicAuth
token = 'API-TOKEN'


df1 = pd.read_csv('rainfall_stations1.csv')
# convert column "a" of a DataFrame
df1["start_year"] = pd.to_numeric(df1["start_year"])
df1["end_year"] = pd.to_numeric(df1["end_year"])
#set static json body values and permsissions
#users needs to exist in agave
body={}
pem1={}
pem1['username']= 'seanbc'
pem1['permission']='ALL'
pem2={}
pem2['username']= 'jgeis'
pem2['permission']='ALL'
pem4={}
pem4['username']= 'ikewai-admin'
pem4['permission']='ALL'
pem5={}
pem5['username']= 'public'
pem5['permission']='READ'

body['name'] = "RainfallStation"
#the schemaID value needs to match your Well schema object UUID in Agave
body['schemaId'] = "6594733581855363561-242ac1110-0001-013"

body['permissions']=[pem1,pem2,pem4,pem5]
#should loop through each dataframe row convert to json and modify to fit well schema
i=0

for i in df1.index:
    j = df1.loc[i].to_json()
    js = json.loads(j)
    #This stores a GeoJSON object in the value.loc field - in Ike Wai this has a spatial index on it in mongodb
    js['loc'] = {"type":"Point", "coordinates":[js['longitude'],js['latitude']]}
    body['value'] = js
    body['geospatial']= True;
    #write out our json to a file for use with the CLI command
    with open('stations/import-station'+str(i)+'.json', 'w') as outfile:
        json.dump(body, outfile)
    #call the CLI to add our well object
    call("./metadata-addupdate -z "+token+" -F stations/import-station"+str(i)+".json", shell=True)
    #createMetadata("9b83a26cab8bd3de68887364c56d832",body)



# In[ ]:
