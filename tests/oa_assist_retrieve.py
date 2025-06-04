import requests
import json

'''Получение ответа от активного ассистента по указанному каналу (thread_id) и 
идентификатору запуска (run_id)'''

url = "http://137.184.87.156:8000/api/oa-assist-retrieve/"
#url = "http://localhost:8000/api/oa-assist-retrieve/"



data = {
    "username": "Alex7",
    "run_id": "run_jPFhYCFQ2X5seHDX3P6o7Ok6",
    "thread_id": "thread_wUUZFBIxyzGbJtVKb1GnrvGb",        
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




# {'status': 'completed', 'message': 'Вот ещё несколько вещей, которые я могу делать:\n\n1. **Конвертация единиц:** Перевод разных измерений, таких как длина, масса или время, из одной единицы в другую.\n\n2. **Поиск информации:** Поиск фактов и данных, предоставление краткой информации по различным вопросам.\n\n3. **Обработка текста:** Проверка грамматики, создание текста, редактирование и другие задачи, связанные с текстом.\n\nЕсли у вас есть конкретный вопрос или задача, дайте знать, и я помогу!', 'response': {'id': 'run_82EI4Loqws42RGiKL5ZGiSHE', 'assistant_id': 'asst_jdGeLjY6ghHPzOjVoXV19jTd', 'cancelled_at': None, 'completed_at': 1748352297, 'created_at': 1748352291, 'expires_at': None, 'failed_at': None, 'incomplete_details': None, 'instructions': 'Ты помощник, который использует числовые функции от разработчика.', 'last_error': None, 'max_completion_tokens': None, 'max_prompt_tokens': None, 'metadata': {}, 'model': 'gpt-4o', 'object': 'thread.run', 'parallel_tool_calls': True, 'required_action': None, 'response_format': 'auto', 'started_at': 1748352294, 'status': 'completed', 'thread_id': 'thread_YT7RwzaGI2LFnkA1xS56HnL6', 'tool_choice': 'auto', 'tools': [{'function': {'name': 'add', 'description': 'Сложить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}, {'function': {'name': 'multiply', 'description': 'Умножить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}], 'truncation_strategy': {'type': 'auto', 'last_messages': None}, 'usage': {'completion_tokens': 115, 'prompt_tokens': 952, 'total_tokens': 1067, 'prompt_token_details': {'cached_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 0}}, 'temperature': 1.0, 'top_p': 1.0, 'tool_resources': {}, 'reasoning_effort': None}}

# {'status': 'requires_action', 'tool_calls': [{'id': 'call_vvjA940EULUUsafMSPr3pBy7', 'function': {'arguments': '{"a":343,"b":543}', 'name': 'add'}, 'type': 'function'}], 'response': {'id': 'run_ViN9MINQMG865krMtpUio0YS', 'assistant_id': 'asst_0dEuPMImhf4oS7fDvhn3QGb3', 'cancelled_at': None, 'completed_at': None, 'created_at': 1748356997, 'expires_at': 1748357597, 'failed_at': None, 'incomplete_details': None, 'instructions': 'Ты помощник, который использует числовые функции от разработчика.', 'last_error': None, 'max_completion_tokens': None, 'max_prompt_tokens': None, 'metadata': {}, 'model': 'gpt-4o', 'object': 'thread.run', 'parallel_tool_calls': True, 'required_action': {'submit_tool_outputs': {'tool_calls': [{'id': 'call_vvjA940EULUUsafMSPr3pBy7', 'function': {'arguments': '{"a":343,"b":543}', 'name': 'add'}, 'type': 'function'}]}, 'type': 'submit_tool_outputs'}, 'response_format': 'auto', 'started_at': 1748356999, 'status': 'requires_action', 'thread_id': 'thread_F7ayXH3Ig7RM98SrGonwctNG', 'tool_choice': 'auto', 'tools': [{'function': {'name': 'add', 'description': 'Сложить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}, {'function': {'name': 'multiply', 'description': 'Умножить два числа', 'parameters': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, 'strict': False}, 'type': 'function'}], 'truncation_strategy': {'type': 'auto', 'last_messages': None}, 'usage': None, 'temperature': 1.0, 'top_p': 1.0, 'tool_resources': {}, 'reasoning_effort': None}}

# call_vvjA940EULUUsafMSPr3pBy7

# call_9DFdPvBNo29pewRHVw54bQ1A