import requests
import json

HDRS = {'Content-type': 'application/json', 'Encoding': 'utf-8'}

def get_info(token, url):
    headers = HDRS.copy()
    headers['Authorization'] = token
    return requests.get(url, verify=True, headers=headers)