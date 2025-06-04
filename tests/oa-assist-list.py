import requests
import json

'''Список Ассистентов'''

url = "http://137.184.87.156:8000/api/oa-assist-list/"
#url = "http://localhost:8000/api/oa-assist-list/"



data = {
    "username": "Alex7" 
}

headers = {
    'appkey': '4a69d997-981d-4808-9053-6ef21e14aa87',
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    data = response.json()
    #print(data)
else:
    print(response.status_code, response.text)


ffg = []
for n in data:
    ffg.append(n.get("id"))

print(ffg)











# [{'id': 'asst_COPL5aj2qksUy81965yLJZWe', 'created_at': 1747830811, 'description': None, 'instructions': 'Ты помощник, который использует числовые функции от разработчика.', 'metadata': {}, 'model': 'gpt-4o', 'name': 'Математик', 'object': 'assistant', 'tools': [{'function': {'name': 'add', 'description': 'Сложить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}, {'function': {'name': 'multiply', 'description': 'Умножить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}], 'response_format': 'auto', 'temperature': 1.0, 'tool_resources': {'code_interpreter': None, 'file_search': None}, 'top_p': 1.0, 'reasoning_effort': None}, {'id': 'asst_UtCUnUUYRHlbDm8n86iFhcXl', 'created_at': 1747744303, 'description': None, 'instructions': 'Ты помощник, который использует числовые функции от разработчика.', 'metadata': {}, 'model': 'gpt-4o', 'name': 'Математик', 'object': 'assistant', 'tools': [{'function': {'name': 'add', 'description': 'Сложить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}, {'function': {'name': 'multiply', 'description': 'Умножить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}], 'response_format': 'auto', 'temperature': 1.0, 'tool_resources': {'code_interpreter': None, 'file_search': None}, 'top_p': 1.0, 'reasoning_effort': None}]

# asst_oknQdhZeCSCuoNZeOKaClNBl
# 
# [asst_oknQdhZeCSCuoNZeOKaClNBl, asst_0Uo9IweqREjLRehN4iKnzbBD, asst_33UzsXY3YTy2HpFBCCZAUH3Q, asst_J4ra2idCxsYDtN977G58Rnsj, asst_Gt1dZFHkljtbnzMgRZ5r9qVW, asst_y9lzkqNP2wCbYi74oquNOQ2n, asst_Hq17xAqnxOoTZ6cBfdsNihuZ, asst_QZODV7v1kj42iJBTAYgkWXCq, asst_0ikTSYYf2HJw7qSeI6fRTGrj, asst_34jFZOrJJFmB0enqXWhr66xC, asst_pEROTgLYnI16qDINIbFp92pC, ]