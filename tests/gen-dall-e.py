import requests

url = "http://137.184.87.156:8000/api/gen-dall-e/"

data = {
        "username": "Shliamb5", # !
        "user_content": "логотип для телеграмм бота, по середине написанно API, в круге, в технологическом тиле, буд то пронизано все проводниками, микросхемы.", # !
        #"quality": "standard", # standard or hd
        "style": "vivid", # vivid ore natural
        #"size": "1024x1024", 
        #"response_format": "url",
        #"n": 1,
        #"model": "dall-e-2"

}

headers = {
    'appkey': 'a36c0e6c-6123-42e9-bcda-1c16e0c7e201',
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)
