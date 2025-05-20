
import requests

image = None

url = "http://137.184.87.156:8000/api/quick-assist-openai/"
#url = "http://localhost:8000/api/quick-assist-openai/"

data = {
        'username': 'Shliamb5', # !
        'user_content': 'Найди сумму чисел 5 и 8',
}

headers = {
    'appkey': 'a36c0e6c-6123-42e9-bcda-1c16e0c7e201',
}


response = requests.post(url, headers=headers, data=data)#, files=image)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)


