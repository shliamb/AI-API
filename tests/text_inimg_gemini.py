import requests

files = None

url = "http://137.184.87.156:8000/api/gemini/"

data = {
        "username": "Shliamb5", # !
        "user_content": "Как называется ее стрижка? Хотя бы примерно.", # !
        "system_content": "Ответь по русски.",
        "model": "gemini-1.5-flash-latest",
}

headers = {
    'appkey': 'a36c0e6c-6123-42e9-bcda-1c16e0c7e201',
}

with open('./uploads/image45.png', 'rb') as file:
    files = {
        'file': ('image45.png', file),  # Необязательно
    }
    response = requests.post(url, headers=headers, data=data, files=files)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)
