import requests
from config import HOST

url = f"http://{HOST}/api/openai-img/"

data = {
        "access_id": "08a898f3-e6dd-49c2-93a7-fff0abc7ad31",
        "user_content": "логотип для телеграмм бота, по середине написанно API, в круге, в технологическом стиле, буд то пронизано все проводниками, микросхемы.", # !
        #"quality": "standard", # standard or hd
        "style": "vivid", # vivid ore natural
        #"size": "1024x1024", 
        #"response_format": "url",
        #"n": 1,
        #"model": "dall-e-2"

}

headers = {
    'some_key': 'd98f74a7-81de-4afd-b06d-94cb6cb821fc',
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)
