




#################################### only text



import requests

# URL API
url = "http://137.184.87.156:8000/api/openai_chat/"
# url = "http://localhost:8000/api/openai/"

data = {
        "username": "Shliamb10", # !
        "user_content": "Привет, сегодня классная погода.", # !
        "system_content": "Ты крутой юморист, каждое слово - шутка",
        "model": "gpt-4o-mini-2024-07-18",
}

headers = {
    'appkey': '72d3d8e8-74c4-4ff6-9033-91e8670b3708',
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print("Успешно отправлено:", response.json())
else:
    print("Ошибка:", response.status_code, response.text)




###################################### + img


import requests


# URL API
url = "http://137.184.87.156:8000/api/openai_chat/"
# url = "http://localhost:8000/api/openai/"

data = {
        "username": "Shliamb10", # !
        "user_content": "Что ты видишь на картинке?", # !
        "model": "gpt-4o-mini-2024-07-18",
}

files = {
    'file': ('image.jpg', open('./uploads/image.jpg', 'rb')),  # !
}

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










'''

Пример текстового + картинка по желанию запроса к API. При отсуствии картинки file = None. Данный endpoint только для текста 
и картинки на выбор в сочитании. Для других файлов есть другой вход. В запросе с картинкой, system_content игнорируется value, но поле необходимо.

API асинхронная, как и библиотека OpenAI. Проверяется в первую очередь username, если оно не верное, то API берет асинхронный тайаут на 5 секунд - тупая защита.
Далее проверяется appkey если оно не верное, начинается отсчет не верных попыток и на пятой попытке предупреждение и блок username а 15 минут. По истичению блокировки 
можно снова попробовать и при успешной попытке - доступ восстановлен. Ограничений по времени обращения к API нету. Величина картинки, кажется не должна привышать 20 mb, 
нужно уточнить в OpenAI документации. Далее проверяется наличиие средств в системе, далее наличие указанной модели в прайсе. После всех проверок, происходит обращение к OpenAI, получение ответа, 
расчет токенов, запись в базу расхода и статистики.


'''