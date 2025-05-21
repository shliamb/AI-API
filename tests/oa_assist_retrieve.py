import requests
import json

'''Получение ответа от активного ассистента по указанному каналу (thread_id) и 
идентификатору запуска (run_id)'''

url = "http://137.184.87.156:8000/api/oa-assist-retrieve/"
#url = "http://localhost:8000/api/oa-assist-retrieve/"



data = {
    "username": "Shliamb5",
    "name": "Математик",
    "run_id": "454",
    "thread_id": "546654",        
}

headers = {
    'appkey': 'a36c0e6c-6123-42e9-bcda-1c16e0c7e201',
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)


