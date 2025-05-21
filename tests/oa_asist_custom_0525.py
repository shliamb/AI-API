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
    "user_content": "умножь 2 и 2",
    "tools": str_tools,
    "assistant_id": "asst_JBoneVMpW2DcjsI9FjxV7FoR",
    "thread_id": "thread_skm9CZ3hFJSGjE9kcQM9sLiR"
}

headers = {
    'appkey': 'a36c0e6c-6123-42e9-bcda-1c16e0c7e201',
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)




# 1 нет асистента и канала {'asist_id': 'asst_aO3gwhPLOwPihaSP26SOIw1T', 'thread_id': 'thread_cKMbVmB5D4f9bjeoFTT8SLoc', 'run_id': 'run_bKTyP4PtQHxyFOWr8BJ8nnG0'} запустил и дал run_id

# 2 нет контента {'asist_id': 'asst_JBoneVMpW2DcjsI9FjxV7FoR', 'thread_id': 'thread_skm9CZ3hFJSGjE9kcQM9sLiR', 'system_message': 'Missing message from user.'} создал асистента и канал и отдал их id

# 3 Еть асистент и канал контент {'asist_id': 'asst_JBoneVMpW2DcjsI9FjxV7FoR', 'thread_id': 'thread_skm9CZ3hFJSGjE9kcQM9sLiR', 'run_id': 'run_ibC2N55iH6RcsjNm3YecHW74'} запустил и дал run_id