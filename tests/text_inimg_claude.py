import requests

image = None

url = "http://137.184.87.156:8000/api/claude/"
# url = "http://localhost:8000/api/claude/"

data = {
        'username': 'Shliamb5', # !
        'user_content': 'Привет Лора, сегодня холодно.', # !
        'system_content': 'Тебя зовут Ева, ты стараешься противоречить всему.',
        'model': 'claude-3-haiku-20240307',
        #'assist_content': '[{"user": "How do I charge my battery?"}, {"assistant": "You should use the provided charging cable."}, {"user": "But it doesn\'t seem to charge."}, {"assistant": "Try another charge.."}]',
}

headers = {
    'appkey': 'a36c0e6c-6123-42e9-bcda-1c16e0c7e201',
}

# with open('./uploads/image.jpg', 'rb') as file:
#     image = {
#         'image': ('image.jpg', file),  # !
#     }

response = requests.post(url, headers=headers, data=data, files=image)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)

