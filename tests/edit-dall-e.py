import requests

image = None

url = "http://137.184.87.156:8000/api/edit-dall-e/"

data = {
        "username": "Shliamb10", # !
        #"size": "1024x1024",
        "user_content": "Дорисуй грустный рот" # !
        #"response_format": "url",
        #"n": 2,
        #"model": "dall-e-2"
}

image = {
    'image': ('edit.png', open('./uploads/edit.png', 'rb')),    # !
    'mask': ('lips.png', open('./uploads/lips.png', 'rb')),     # это странно себя ведет, не понятно пока что..
}

headers = {
    'appkey': '72d3d8e8-74c4-4ff6-9033-91e8670b3708',
}

response = requests.post(url, headers=headers, data=data, files=image)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)