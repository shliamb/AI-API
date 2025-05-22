import requests
import json

'''Удаление тредс по id'''

url = "http://137.184.87.156:8000/api/oa-thread-del/"
#url = "http://localhost:8000/api/oa-thread-del/"



data = {
    "username": "Shliamb5",
    "thread_id": "thread_kdnhJrhkFpvfZNR8QljlzmZT",        
}

headers = {
    'appkey': 'a36c0e6c-6123-42e9-bcda-1c16e0c7e201',
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)

# {'id': 'thread_skm9CZ3hFJSGjE9kcQM9sLiR', 'deleted': True, 'object': 'thread.deleted'}