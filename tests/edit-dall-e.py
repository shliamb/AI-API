import requests
import json


image = None
mask = None

# URL API
url = "http://137.184.87.156:8000/api/edit-dall-e/"
# url = "http://localhost:8000/api/openai/"

data = {
        "username": "Shliamb10", # !
        #"size": "1024x1024",
        "user_content": "Дорисуй грустный рот" # !
        #"response_format": "url",
        #"n": 2,
        #"model": "dall-e-2"

}

# Данные для отправки
image = {
    'image': ('edit.png', open('./uploads/edit.png', 'rb')), # !
    'mask': ('lips.png', open('./uploads/lips.png', 'rb')), # это странно себя ведет, не понятно пока что..
}


# Заголовки запроса multipart/form-data, Content-Type выставляет библиотека request автоматом
headers = {
    'appkey': '72d3d8e8-74c4-4ff6-9033-91e8670b3708',
}

# Отправка POST-запроса
response = requests.post(url, headers=headers, data=data, files=image)

# Проверка статуса ответа и вывод результата
if response.status_code == 200:
    print("Успешно отправлено:", response.json())
else:
    print("Ошибка:", response.status_code, response.text)