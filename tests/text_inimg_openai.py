
import requests

image = None

url = "http://137.184.87.156:8000/api/openai_chat/"
# url = "http://localhost:8000/api/openai_chat/"

data = {
        'username': 'Shliamb5', # !
        'user_content': 'Что на рисунке видишь?', # !
        'system_content': 'Ты крутой юморист, каждое слово - шутка',
        'model': 'gpt-4o-mini-2024-07-18',
        'assist_content': '[{"user": "How do I charge my battery?"}, {"assistant": "You should use the provided charging cable."}, {"user": "But it doesn\'t seem to charge."}, {"assistant": "Try another charge.."}]',
        #'response_format': '{"type":"json_schema","json_schema":{"name":"user_profile","schema":{"type":"object","properties":{"name":{"description":"The name of the user","type":"string"},"age":{"description":"The age of the user","type":"integer"},"interests":{"description":"List of users interests","type":"array","items":{"type":"string"}}},"required":["name","age","interests"]}}}',
        #'response_format': '{"type": "json_object"}' # if not,  response_format is {"type": "text"}
}

headers = {
    'appkey': 'a36c0e6c-6123-42e9-bcda-1c16e0c7e201',
}

with open('./uploads/image.jpg', 'rb') as file:
    image = {
        'image': ('image.jpg', file),  # !
    }

    response = requests.post(url, headers=headers, data=data, files=image)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)





# "But it doesn't seem to charge."

    #response_format = {"type":"json_schema","json_schema":{"name":"user_profile","schema":{"type":"object","properties":{"name":{"description":"The name of the user","type":"string"},"age":{"description":"The age of the user","type":"integer"},"interests":{"description":"List of users interests","type":"array","items":{"type":"string"}}},"required":["name","age","interests"]}}}
    #response_format = {"type": "text"}
    #response_format = {"type": "json_object"}
'''

Пример текстового + картинка по желанию запроса к API. При отсуствии картинки file = None. Данный endpoint только для текста 
и картинки на выбор в сочитании. Для других файлов есть другой вход. В запросе с картинкой, system_content игнорируется value, но поле необходимо.

API асинхронная, как и библиотека OpenAI. Проверяется в первую очередь username, если оно не верное, то API берет асинхронный тайаут на 5 секунд - тупая защита.
Далее проверяется appkey если оно не верное, начинается отсчет не верных попыток и на пятой попытке предупреждение и блок username а 15 минут. По истичению блокировки 
можно снова попробовать и при успешной попытке - доступ восстановлен. Ограничений по времени обращения к API нету. Величина картинки, кажется не должна привышать 20 mb, 
нужно уточнить в OpenAI документации. Далее проверяется наличиие средств в системе, далее наличие указанной модели в прайсе. После всех проверок, происходит обращение к OpenAI, получение ответа, 
расчет токенов, запись в базу расхода и статистики.


'''