from flask import Flask, jsonify, request
import requests
import json

import pandas as pd 
df = pd.read_excel("input\df_result_netherlands_1.xlsx")
print(df.shape)
print(df.info())

#myobj = {"name":df['company_name'],"linkedin_url":df['compnay_url']}

mydict = dict(zip(df.company_name, df.compnay_url))
#URL = "https://controller.nl/api/v1/companies?key=0atfX7IJ5I"
"""
x = requests.post(URL, json = myobj)

print(x.text)
"""