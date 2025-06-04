import requests
import json

'''Возврат результата Агенту'''

url = "http://137.184.87.156:8000/api/oa-return-result-assist/"
#url = "http://localhost:8000/api/oa-return-result-assist/"

# tool_outputs_json = [
#     {
#         "tool_call_id": "call_EpJJE0HYIwyPItdIktSqZrBs",
#         "output": "end"
#     }#,
#     # {
#     #     "tool_call_id": "3565464",
#     #     "output": None
#     # }
# ]

tool_outputs_json = [{'tool_call_id': 'call_CRh331p3anxtWUWhDgY4o2wf', 'output': 'пока'}]


tool_outputs_str = json.dumps(tool_outputs_json, ensure_ascii=False)

data = {
    "username": "Alex7",
    "run_id": "run_4aPVxiUhfHJe52BYb27MVBgA",
    "thread_id": "thread_xOBBWj3IpCYj11z51apwhlv5",
    "tool_outputs": tool_outputs_str  
}

headers = {
    'appkey': '4a69d997-981d-4808-9053-6ef21e14aa87'
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)



# {'id': 'run_Td5hNVh1UmqaIkh3yUk3fQjq', 'assistant_id': 'asst_ico0V2EH6M2AMd9EdJzvdlN0', 'cancelled_at': None, 'completed_at': None, 'created_at': 1748361125, 'expires_at': 1748361725, 'failed_at': None, 'incomplete_details': None, 'instructions': 'Ты помощник, который использует числовые функции от разработчика.', 'last_error': None, 'max_completion_tokens': None, 'max_prompt_tokens': None, 'metadata': {}, 'model': 'gpt-4o', 'object': 'thread.run', 'parallel_tool_calls': True, 'required_action': None, 'response_format': 'auto', 'started_at': 1748361129, 'status': 'queued', 'thread_id': 'thread_wUUZFBIxyzGbJtVKb1GnrvGb', 'tool_choice': 'auto', 'tools': [{'function': {'name': 'add', 'description': 'Сложить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}, {'function': {'name': 'multiply', 'description': 'Умножить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}], 'truncation_strategy': {'type': 'auto', 'last_messages': None}, 'usage': None, 'temperature': 1.0, 'top_p': 1.0, 'tool_resources': {}, 'reasoning_effort': None}

