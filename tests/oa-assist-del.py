import requests
import json
import time

'''Удаление Ассистента по id'''

url = "http://137.184.87.156:8000/api/oa-assist-del/"
#url = "http://localhost:8000/api/oa-assist-del/"


sdd = ['asst_rqiMWlxFkrhNZgvQinfqMV55']


for n in sdd:

    data = {
        "username": "Alex7",
        "assistant_id": n,        
    }

    headers = {
        'appkey': '4a69d997-981d-4808-9053-6ef21e14aa87',
    }





    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print(response.json())
    else:
        print(response.status_code, response.text)

    time.sleep(3)


print("Done")

# {'id': 'asst_aO3gwhPLOwPihaSP26SOIw1T', 'deleted': True, 'object': 'assistant.deleted'}


