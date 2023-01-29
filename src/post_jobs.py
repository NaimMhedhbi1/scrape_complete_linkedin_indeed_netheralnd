from flask import Flask, jsonify, request
import requests
import json
import pandas as pd 
import textwrap
import re
df = pd.read_excel(r"output\df_result_netherlands_with_IDS_1.xlsx")
#df = df[20:]
df1 = df[['company_ID','jobtype_id','job_title','apply_by_form','job_url','job_summary']]
df1 =  df1.rename(columns={'company_ID':'company_id','job_title':'title','job_summary':'description_html','job_url':'apply_url'})
json_list = json.loads(json.dumps(list(df1.T.to_dict().values())))
URL = "https://controller.nl/api/v1/jobs?key=0atfX7IJ5I"
for i in range(len(json_list)):
        x = requests.post(URL, json = json_list[i])
        print(x.text)

