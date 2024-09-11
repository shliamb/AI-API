import requests

files = None

# URL API
url = "http://137.184.87.156:8000/api/gemini/"
# url = "http://localhost:8000/api/openai/"

data = {
        "username": "Shliamb10", # !
        "user_content": "Как называется ее стрижка? Хотя бы примерно.", # !
        "system_content": "Ответь по русски.",
        "model": "gemini-1.5-flash-latest",
}

# Данные для отправки
files = {
    'file': ('image45.png', open('./uploads/image45.png', 'rb')),  # Необязательно
}

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