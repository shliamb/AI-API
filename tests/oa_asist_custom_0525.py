import requests
import json

"""

    Если указаны assistant_id и thread_id — используется существующий ассистент и поток.  
    Если одного из параметров нет — недостающее создаётся автоматически.  

    Если передан user_content, сообщение отправляется в поток, и запускается выполнение ассистента (run).  
    Если user_content отсутствует — выполнение не инициируется, возвращаются только assistant_id и thread_id.  

    Ответ в любом случае содержит:  
    - assistant_id  
    - thread_id  
    - run_id (только если был запущен run)

"""

url = "http://137.184.87.156:8000/api/oa-assist-custom-0525/"
#url = "http://localhost:8000/api/oa-assist-custom-0525/"

tools=[
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Сложить два числа", 
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Умножить два числа",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

str_tools = json.dumps(tools, ensure_ascii=False)


data = {
    "username": "Shliamb5",
    "name": "Математик",
    "instructions": "Ты помощник, который использует числовые функции от разработчика.",
    "model": "gpt-4o",        
    "user_content": "Найди сумму чисел 5 и 8",
    "tools": str_tools,
    "assistant_id": None,
    "thread_id": None
}

headers = {
    'appkey': 'a36c0e6c-6123-42e9-bcda-1c16e0c7e201',
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)





#List assist: [Assistant(id='asst_UtCUnUUYRHlbDm8n86iFhcXl', created_at=1747744303, description=None, instructions='Ты помощник, который использует числовые функции от разработчика.', metadata={}, model='gpt-4o', name='Математик', object='assistant', tools=[FunctionTool(function=FunctionDefinition(name='add', description='Сложить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function'), FunctionTool(function=FunctionDefinition(name='multiply', description='Умножить два числа', parameters={'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}, strict=False), type='function')], response_format='auto', temperature=1.0, tool_resources=ToolResources(code_interpreter=None, file_search=None), top_p=1.0, reasoning_effort=None)]