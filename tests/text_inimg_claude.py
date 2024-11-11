import requests

image = None

url = "http://137.184.87.156:8000/api/claude/"
# url = "http://localhost:8000/api/claude/"

data = {
        'username': 'Shliamb10', # !
        'user_content': 'Что на рисунке видишь?', # !
        'system_content': 'Ты крутой юморист, каждое слово - шутка',
        'model': 'claude-3-haiku-20240307',
        #'assist_content': '[{"user": "How do I charge my battery?"}, {"assistant": "You should use the provided charging cable."}, {"user": "But it doesn\'t seem to charge."}, {"assistant": "Try another charge.."}]',
}

headers = {
    'appkey': '72d3d8e8-74c4-4ff6-9033-91e8670b3708',
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

