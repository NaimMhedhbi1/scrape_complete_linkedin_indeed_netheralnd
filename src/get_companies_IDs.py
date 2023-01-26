from flask import Flask, jsonify, request
import requests
import json
import pandas as pd 
from json import loads

df = pd.read_excel(r"C:\Users\121\Documents\vscode\input\df_result_netherlands_1.xlsx")
URL = "https://controller.nl/api/v1/companies?key=0atfX7IJ5I"
x = requests.get(URL)

dic = loads(x.text)
print(dic)
dic = pd.DataFrame(dic)
dic = dic.explode('results')
dic = dic['results'].apply(pd.Series)
df_ids = dic[['name','id']]
df_ids =  df_ids.rename(columns={'company_name': 'name'})
df_ids = df_ids.reset_index()
del df_ids['index']
df_ids = df_ids.dropna()
df_ids['id'] = df_ids['id'].astype(int)

df['company_ID']=df.company_name.map(dict(zip(df_ids.name,df_ids.id))) #mapping companies to their IDS extracted


df.to_excel('output/df_result_netherlands_with_IDS.xlsx',index = False)
