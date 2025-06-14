import requests
from config import HOST

path_file = None

# path_file = "./uploads/image.jpg"

url = f"http://{HOST}/api/openai-chat/"

data = {
        "access_id": "39d092a8-23e4-4684-91cf-ec9cd1d50790",
        "user_content": "Что на рисунке видишь?",
        "system_content": "Ты крутой юморист, каждое слово - шутка",
        "model": "gpt-4o-mini-2024-07-18",
        #"assist_content": '[{"user": "How do I charge my battery?"}, {"assistant": "You should use the provided charging cable."}, {"user": "But it doesn\'t seem to charge."}, {"assistant": "Try another charge.."}]',
        #'response_format': '{"type":"json_schema","json_schema":{"name":"user_profile","schema":{"type":"object","properties":{"name":{"description":"The name of the user","type":"string"},"age":{"description":"The age of the user","type":"integer"},"interests":{"description":"List of users interests","type":"array","items":{"type":"string"}}},"required":["name","age","interests"]}}}',
        #'response_format': '{"type": "json_object"}' # if not,  response_format is {"type": "text"}
}

headers = {
    "appkey": "a9446aa4-cf9a-461e-898c-fce4d84efc01",
}

if path_file:
    with open(path_file, 'rb') as f:
        file = {'file': ('image.jpg', f)}
        response = requests.post(url, headers=headers, data=data, files=file)
else:
    response = requests.post(url, headers=headers, data=data)



if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)

