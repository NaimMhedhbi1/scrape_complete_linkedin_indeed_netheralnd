#added the jobtype_id mapping
from flask import Flask, jsonify, request
import requests
import json
import pandas as pd 
from json import loads

df = pd.read_excel(r"C:\Users\121\Documents\vscode\input\df_result_netherlands_2.xlsx")
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


df.work_time = df.work_time.str.replace(r'Full-time · Associate', r'Full time')
df.work_time = df.work_time.str.replace(r'Full-time · Mid-Senior level', r'Full time')
df.work_time = df.work_time.str.replace(r'Full-time · Director', r'Full time')

df.work_time = df.work_time.str.replace(r'Full-time', r'Full time')
df.work_time = df.work_time.str.replace(r'Full time · Entry level', r'Full time')
df.work_time = df.work_time.str.replace(r'€3,600/month - €5,200/month · Full time', r'Full time')
df.work_time = df.work_time.str.replace(r'Full time · Internship', r'Internship')
df.work_time = df.work_time.str.replace(r'Part-time · Associate', r'Part time')
df.work_time = df.work_time.str.replace(r'Part-time', r'Part time')
df.work_time = df.work_time.str.replace(r'Contract · Mid-Senior level', r'Contract')
df.work_time = df.work_time.str.replace(r'Contract · Director', r'Contract')
# initialize list of lists
data = [['Contract', 10889], ['Interim', 10504], ['Internship', 10479],['Freelance', 10478],['Part time', 10477],['Full time', 10476]]
  
# Create the pandas DataFrame
data = pd.DataFrame(data, columns=['work_time', 'jobtype_id'])
  
# print dataframe.
df['jobtype_id']=df.work_time.map(dict(zip(data.work_time,data.jobtype_id)))

df.to_excel('output/df_result_netherlands_with_IDS_1.xlsx',index = False)
