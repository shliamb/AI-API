import requests
import json

# URL API
url = "http://137.184.87.156:8000/api/variations-dall-e/"
# url = "http://localhost:8000/api/openai/"

data = {
        "username": "Shliamb10",        # !
        "size": "1024x1024",            # 
        "response_format": "url",       #
        "n": 1,                         #
        "model": "dall-e-2"             # 

}


# Данные для отправки
files = {
    'file': ('image45.png', open('./uploads/image45.png', 'rb')),   # !
}

# files = None

# Заголовки запроса multipart/form-data, Content-Type выставляет библиотека request автоматом
headers = {
    'appkey': '72d3d8e8-74c4-4ff6-9033-91e8670b3708',
}

# Отправка POST-запроса
response = requests.post(url, headers=headers, data=data, files=files)


# Проверка статуса ответа и вывод результата
if response.status_code == 200:
    print("Успешно отправлено:", response.json())
else:
    print("Ошибка:", response.status_code, response.text)