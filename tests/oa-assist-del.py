import requests
import json

'''Удаление Ассистента по id'''

url = "http://137.184.87.156:8000/api/oa-assist-del/"
#url = "http://localhost:8000/api/oa-assist-del/"



data = {
    "username": "Shliamb5",
    "assistant_id": "asst_UtCUnUUYRHlbDm8n86iFhcXl",        
}

headers = {
    'appkey': 'a36c0e6c-6123-42e9-bcda-1c16e0c7e201',
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)

# {'id': 'asst_aO3gwhPLOwPihaSP26SOIw1T', 'deleted': True, 'object': 'assistant.deleted'}