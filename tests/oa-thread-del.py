import requests
import json

'''Удаление тредс по id'''

url = "http://137.184.87.156:8000/api/oa-thread-del/"
#url = "http://localhost:8000/api/oa-thread-del/"



data = {
    "username": "Alex7",
    "thread_id": "thread_rJPiJyIg7vnloIB7Ed52YFi0",        
}

headers = {
    'appkey': '4a69d997-981d-4808-9053-6ef21e14aa87',
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)

# {'id': 'thread_skm9CZ3hFJSGjE9kcQM9sLiR', 'deleted': True, 'object': 'thread.deleted'}