import requests
import json

'''Список Ассистентов'''

url = "http://137.184.87.156:8000/api/oa-assist-list/"
#url = "http://localhost:8000/api/oa-assist-list/"



data = {
    "username": "Shliamb5" 
}

headers = {
    'appkey': 'a36c0e6c-6123-42e9-bcda-1c16e0c7e201',
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)


# [{'id': 'asst_COPL5aj2qksUy81965yLJZWe', 'created_at': 1747830811, 'description': None, 'instructions': 'Ты помощник, который использует числовые функции от разработчика.', 'metadata': {}, 'model': 'gpt-4o', 'name': 'Математик', 'object': 'assistant', 'tools': [{'function': {'name': 'add', 'description': 'Сложить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}, {'function': {'name': 'multiply', 'description': 'Умножить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}], 'response_format': 'auto', 'temperature': 1.0, 'tool_resources': {'code_interpreter': None, 'file_search': None}, 'top_p': 1.0, 'reasoning_effort': None}, {'id': 'asst_UtCUnUUYRHlbDm8n86iFhcXl', 'created_at': 1747744303, 'description': None, 'instructions': 'Ты помощник, который использует числовые функции от разработчика.', 'metadata': {}, 'model': 'gpt-4o', 'name': 'Математик', 'object': 'assistant', 'tools': [{'function': {'name': 'add', 'description': 'Сложить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}, {'function': {'name': 'multiply', 'description': 'Умножить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}], 'response_format': 'auto', 'temperature': 1.0, 'tool_resources': {'code_interpreter': None, 'file_search': None}, 'top_p': 1.0, 'reasoning_effort': None}]