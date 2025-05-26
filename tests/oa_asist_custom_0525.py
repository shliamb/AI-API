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
    "username": "Alex7",
    "name": "Математик",
    "instructions": "Ты помощник, который использует числовые функции от разработчика.",
    "model": "gpt-4o",        
    "user_content": "Ты готов к работе?",
    "tools": str_tools,
    "assistant_id": "asst_jdGeLjY6ghHPzOjVoXV19jTd",
    "thread_id": "thread_YT7RwzaGI2LFnkA1xS56HnL6"
}

headers = {
    'appkey': '4a69d997-981d-4808-9053-6ef21e14aa87',
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)




# 1 нет асистента и канала {'asist_id': 'asst_aO3gwhPLOwPihaSP26SOIw1T', 'thread_id': 'thread_cKMbVmB5D4f9bjeoFTT8SLoc', 'run_id': 'run_bKTyP4PtQHxyFOWr8BJ8nnG0'} запустил и дал run_id

# 2 нет контента {'asist_id': 'asst_JBoneVMpW2DcjsI9FjxV7FoR', 'thread_id': 'thread_skm9CZ3hFJSGjE9kcQM9sLiR', 'system_message': 'Missing message from user.'} создал асистента и канал и отдал их id

# 3 Еть асистент и канал контент {'asist_id': 'asst_JBoneVMpW2DcjsI9FjxV7FoR', 'thread_id': 'thread_skm9CZ3hFJSGjE9kcQM9sLiR', 'run_id': 'run_ibC2N55iH6RcsjNm3YecHW74'} запустил и дал run_id




# {'asist_id': 'asst_vnwqU4a8930ZSHmZMlxRrfKp', 'thread_id': 'thread_kdnhJrhkFpvfZNR8QljlzmZT', 'push_message': True, 'run_id': 'run_I3iuAbuccCBNixSnj9hGLKVq'}

# {'asist_id': 'asst_xvtv85TFfs1WHgtcYp6Kl5fE', 'thread_id': 'thread_rJPiJyIg7vnloIB7Ed52YFi0', 'push_message': True, 'run_id': 'run_beUPVVrREjPcOxQsC4KlXjkl'}