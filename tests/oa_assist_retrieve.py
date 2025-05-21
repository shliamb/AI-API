import requests
import json

'''Получение ответа от активного ассистента по указанному каналу (thread_id) и 
идентификатору запуска (run_id)'''

url = "http://137.184.87.156:8000/api/oa-assist-retrieve/"
#url = "http://localhost:8000/api/oa-assist-retrieve/"



data = {
    "username": "Shliamb5",
    "run_id": "run_ibC2N55iH6RcsjNm3YecHW74",
    "thread_id": "thread_skm9CZ3hFJSGjE9kcQM9sLiR",        
}

headers = {
    'appkey': 'a36c0e6c-6123-42e9-bcda-1c16e0c7e201',
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)

# ['requires_action', [{'id': 'call_wwHvZu4dnrkouBBgL92c9ZY7', 'function': {'arguments': '{"a":5,"b":8}', 'name': 'add'}, 'type': 'function'}]]
