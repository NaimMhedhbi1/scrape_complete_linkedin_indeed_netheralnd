from flask import Flask, jsonify, request
import requests
import json
import pandas as pd 

df = pd.read_excel("input\df_result_netherlands_2.xlsx")
#df = df.iloc[[1,3]]
df = df.drop_duplicates(subset='company_location', keep="first")
print(df.shape)

print(df.info())
#df.compnay_url = df.compnay_url.str.replace(r'life/', r'')
#df['compnay_url']=df['compnay_url'].astype(str)
df1 = df[['company_location']]
df1 =  df1.rename(columns={'company_location': 'name'})
json_list = json.loads(json.dumps(list(df1.T.to_dict().values())))
URL = "https://controller.nl/api/v1/locations?key=0atfX7IJ5I"
for i in range(len(json_list)):
    try:

        x = requests.post(URL, json = json_list[i])
        print(x.text)
    except:
        pass 

