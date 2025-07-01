# import requests
# from config import HOST

# path_file = None

# # path_file = "./uploads/image.jpg"

# url = f"http://{HOST}/api/openai-chat/"

# PROXIES = {
#     "http": "http://14a368e1f0fb8:3f48aeba51@45.149.100.135:12323"
#     #"https": "http://14a368e1f0fb8:3f48aeba51@45.149.100.135:12323",  # желательно добавить и для HTTPS
# }

# data = {
#         "access_id": "a66c5349-e2df-47a8-919f-3570c521872d",
#         "user_content": "Что на рисунке видишь?",
#         "system_content": "Ты крутой юморист, каждое слово - шутка",
#         "model": "gpt-4o-mini-2024-07-18",
#         #"assist_content": '[{"user": "How do I charge my battery?"}, {"assistant": "You should use the provided charging cable."}, {"user": "But it doesn\'t seem to charge."}, {"assistant": "Try another charge.."}]',
#         #'response_format': '{"type":"json_schema","json_schema":{"name":"user_profile","schema":{"type":"object","properties":{"name":{"description":"The name of the user","type":"string"},"age":{"description":"The age of the user","type":"integer"},"interests":{"description":"List of users interests","type":"array","items":{"type":"string"}}},"required":["name","age","interests"]}}}',
#         #'response_format': '{"type": "json_object"}' # if not,  response_format is {"type": "text"}
# }

# headers = {
#     'appkey': '4af25a70-29d8-4a1e-8b68-f582014305c7',
# }

# if path_file:
#     with open(path_file, 'rb') as f:
#         file = {'file': ('image.jpg', f)}
#         response = requests.post(url, headers=headers, data=data, files=file)
# else:
#     response = requests.post(url, headers=headers, data=data, proxies=PROXIES)



# if response.status_code == 200:
#     print(response.json())
# else:
#     print(response.status_code, response.text)



import requests
import aiohttp
import asyncio

from config import HOST#, ACCESS_ID, API_KEY, VALUE_KEY, PROXIES

path_file = None
#proxies = None

PROXIES = {
    "http": "http://14a368e1f0fb8:3f48aeba51@45.149.100.135:12323"
    #"https": "http://14a368e1f0fb8:3f48aeba51@45.149.100.135:12323",  # желательно добавить и для HTTPS
}

# path_file = "./uploads/image.jpg"

async def main():
    url = f"http://{HOST}/api/openai-chat/"

    data = {
        "access_id": "a66c5349-e2df-47a8-919f-3570c521872d",
        #"access_id": ACCESS_ID, # ACCESSID (или любой токен) безопаснее передавать в заголовке Authorization      Пример: headers["Authorization"] = f"Bearer {ACCESSID}". 
        "user_content": "Ты сегодня не добрая)",
        "system_content": "Ты девушка 27 лет",
        "model": "gpt-4o-mini",
    }

    headers = {
        'appkey' : '4af25a70-29d8-4a1e-8b68-f582014305c7',
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }


    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers, proxy=PROXIES) as resp:
            print(resp.status)
            resp_text = await resp.text()
            print(resp_text)

asyncio.run(main())

