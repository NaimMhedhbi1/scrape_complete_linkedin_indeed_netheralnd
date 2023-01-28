from flask import Flask, jsonify, request
import requests
import json
import pandas as pd 

df = pd.read_excel(r"output\df_result_netherlands_with_IDS_1.xlsx")
df = df.iloc[[8,10]]
try: 
    df['email'] =df['email'].str.split(' ', 1).str[0].str.strip()
    
except:
    pass
df['email'] = df['email'].fillna('not_found_email@controller.nl')

df['apply_by_form']='false'
df.job_summary = df.job_summary.str.replace(r'.', r'. ')
print(df.shape)


print(df.info())
df1 = df[['company_ID','jobtype_id','job_title','apply_by_form','job_url','job_summary','email']]
df1 =  df1.rename(columns={'company_ID':'company_id','job_title':'title','job_summary':'description_html','job_url':'apply_url','email':'apply_email'})
json_list = json.loads(json.dumps(list(df1.T.to_dict().values())))
URL = "https://controller.nl/api/v1/jobs?key=0atfX7IJ5I"
for i in range(len(json_list)):
        x = requests.post(URL, json = json_list[i])
        print(x.text)

