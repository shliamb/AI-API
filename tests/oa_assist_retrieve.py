import requests
import json

'''Получение ответа от активного ассистента по указанному каналу (thread_id) и 
идентификатору запуска (run_id)'''

url = "http://137.184.87.156:8000/api/oa-assist-retrieve/"
#url = "http://localhost:8000/api/oa-assist-retrieve/"



data = {
    "username": "Alex7",
    "run_id": "run_aQ9sf8aXIPj5PoN5srZlCzRw",
    "thread_id": "thread_YT7RwzaGI2LFnkA1xS56HnL6",        
}

headers = {
    'appkey': '4a69d997-981d-4808-9053-6ef21e14aa87'
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)

# ['requires_action', [{'id': 'call_wwHvZu4dnrkouBBgL92c9ZY7', 'function': {'arguments': '{"a":5,"b":8}', 'name': 'add'}, 'type': 'function'}]]
