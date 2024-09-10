# https://github.com/google-gemini/generative-ai-python/blob/main/google/generativeai/answer.py

# Base
import logging
import aiohttp
import asyncio
import base64
# Google
# import google.generativeai as genai
# import PIL.Image
# Service
from keys import API_KEY_GEMINI, is_admin
from general_functions import calculation


# genai.configure(api_key=api_key_gemini)


# # Main Text Google Function
# async def mod_gemini(description, image_path):

#     try:
#         username = description.get("username")
#         user_content = description.get("user_content")
#         system_content = description.get("system_content")
#         model_name = description.get("model")
#         # tools = description.get("tools")


#         model = genai.GenerativeModel(
#             model_name = model_name,
#             # tools = user_input.tools or None, # "tools": "code_execution",
#             system_instruction = system_content or None
#         )

#         if not image_path:
#             response = model.generate_content(user_content)

#         if image_path:
#             organ = PIL.Image.open(image_path)
#             response = model.generate_content([user_content, organ])

#         # Tokens:
#         if response:
#             usage_metadata = response.usage_metadata
#             total_token_count = usage_metadata.total_token_count
#             logging.info(f"Gemini text in tokens: {str(model.count_tokens(user_content))}")
#             logging.info(f"Gemini all text tokens: {str(response.usage_metadata)}")
#         else:
#             logging.error("No response from Google Gemini.")
#             return {"response": "No response from Google Gemini."}
        
#         model_version = model_name
#         used_tokens = total_token_count


#         # Calculation of money spent on tokens
#         expenses = await calculation(username, model_version, used_tokens, input_data="text")

#         return {"response": response.text, "expenses": expenses, "used_tokens": used_tokens}
    
#     except Exception as e:
#        logging.error(f"Error is: {e}")
#        return {"Error:": e} # Ни одну ошибку не показывает тварь!!!













# Main Text Google Function
async def mod_gemini(description, image_path): # description, image_path


    username = description.get("username")
    user_content = description.get("user_content")
    system_content = description.get("system_content")
    model_name = description.get("model")
    # tools = description.get("tools")



    # URL API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY_GEMINI}"

    headers = {
        'Content-Type': 'application/json'
    }

    img_path = image_path

    with open(img_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # data = {
    #     "contents": [{
    #         "parts": [
    #             {"text": user_content},
    #             {
    #                 "inline_data": {
    #                     "mime_type": "image/jpeg",
    #                     "data": encoded_image
    #                 }
    #             }
    #         ]
    #     }]
    # }



    data = {
                "contents": [
                    # {
                    #     "role": "system",
                    #     "parts": [
                    #         {
                    #             "text": system_content
                    #         }
                    #     ]
                    # },
                    {
                        "role": "model",
                        "parts": [
                            {
                                "text": model_name
                            },
                        ]
                    },
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": user_content
                            },
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": encoded_image
                                }
                            }
                        ]
                    }
                ]
            }





    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            print(await response.json())
            return await response.json()

if __name__ == "__main__":
    asyncio.run(mod_gemini())







'''
https://ai.google.dev/api/files?hl=ru#v1beta.media.upload


Gemini 1.5 Pro и 1.5 Flash поддерживают максимум 3600 файлов изображений.

Изображения должны относиться к одному из следующих типов MIME данных изображения:

PNG - image/png
JPEG — image/jpeg
WEBP — image/webp
HEIC — image/heic
HEIF - image/heif
Каждое изображение эквивалентно 258 токенам.



'''































# import PIL.Image

# model = genai.GenerativeModel("gemini-1.5-flash")
# organ = PIL.Image.open(media / "organ.jpg")
# response = model.generate_content(["Tell me about this instrument", organ])
# print(response.text)




# async def generate_content():
#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
#     api_key = api_key_gemini
#     headers = {
#         'Content-Type': 'application/json'
#     }
    
#     data = {
#         "contents": [{
#             "parts": [{"text": "Write a story about a magic backpack."}]
#         }]
#     }

#     async with aiohttp.ClientSession() as session:
#         async with session.post(f"{url}?key={api_key}", json=data, headers=headers) as response:
#             if response.status == 200:
#                 result = await response.json()
#                 print(result)
#             else:
#                 print(f"Error: {response.status} - {await response.text()}")

# # Запуск асинхронной функции
# if __name__ == "__main__":
#     asyncio.run(generate_content())








# import os
# import subprocess
# import requests
# import json

# # Задайте переменные
# IMG_PATH_2 = './uploads/image.jpg'  # Путь к изображению
# BASE_URL = 'https://your_base_url.com'  # URL вашей базы
# GOOGLE_API_KEY = api_key_gemini  # Ваш Google API ключ

# # Получение MIME типа и количества байт
# MIME_TYPE = subprocess.check_output(['file', '-b', '--mime-type', IMG_PATH_2]).decode('utf-8').strip()
# NUM_BYTES = os.path.getsize(IMG_PATH_2)
# DISPLAY_NAME = "TEXT"

# # Начальная резюмируемая просьба, определяющая метаданные.
# headers_start = {
#     "X-Goog-Upload-Protocol": "resumable",
#     "X-Goog-Upload-Command": "start",
#     "X-Goog-Upload-Header-Content-Length": str(NUM_BYTES),
#     "X-Goog-Upload-Header-Content-Type": MIME_TYPE,
#     "Content-Type": "application/json"
# }

# data_start = json.dumps({'file': {'display_name': DISPLAY_NAME}})

# response_start = requests.post(
#     f"{BASE_URL}/upload/v1beta/files?key={GOOGLE_API_KEY}",
#     headers=headers_start,
#     data=data_start
# )

# upload_url = response_start.headers.get("X-Goog-Upload-URL")

# # Загрузка фактических байтов.
# headers_upload = {
#     "Content-Length": str(NUM_BYTES),
#     "X-Goog-Upload-Offset": "0",
#     "X-Goog-Upload-Command": "upload, finalize"
# }

# with open(IMG_PATH_2, 'rb') as img_file:
#     response_upload = requests.post(upload_url, headers=headers_upload, data=img_file)

# # Получение URI файла из ответа загрузки.
# file_info_json = response_upload.json()
# file_uri = file_info_json['file']['uri']
# print(f"file_uri={file_uri}")

# # Теперь генерируем контент с использованием этого файла.
# generate_content_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
# data_generate_content = {
#     "contents": [{
#         "parts": [
#             {"text": "Can you tell me about the instruments in this photo?"},
#             {"file_data": {"mime_type": MIME_TYPE, "file_uri": file_uri}}
#         ]
#     }]
# }

# response_generate_content = requests.post(generate_content_url, headers={'Content-Type': 'application/json'}, json=data_generate_content)
# response_json = response_generate_content.json()

# print(json.dumps(response_json, indent=4))  # Печать всего ответа в читаемом виде.

# if 'candidates' in response_json:
#     for candidate in response_json['candidates']:
#         for part in candidate['content']['parts']:
#             if 'text' in part:
#                 print(part['text'])  # Печать текста кандидатов.





















#         model = genai.GenerativeModel(
#             model_name = model_name,
#             # tools = user_input.tools or None, # "tools": "code_execution",
#             system_instruction = system_content or None
#         )

#         if not image_path:
#             response = model.generate_content(user_content)













# async def generate_content():
#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
#     api_key = api_key_gemini
    
#     # Подготовка текстовой части запроса
#     # text_data = {
#     #     "contents": [{
#     #         "parts": [{"text": "Write a story about a magic backpack."}]
#     #     }]
#     # }


#     text_data = "Write a story about a magic backpack."

#     # Подготовка файла изображения
#     # image_path = './uploads/image.jpg'  # Укажите путь к вашему изображению



#     async with aiohttp.ClientSession() as session:
#         # with open(image_path, 'rb') as image_file:
#         #     form_data = aiohttp.FormData()
#         #     form_data.add_field('json', 
#         #                         value=aiohttp.JsonPayload(text_data), 
#         #                         content_type='application/json')
#         #     form_data.add_field('file', 
#         #                         image_file, 
#         #                         filename='image.jpg',
#         #                         content_type='image/jpeg')

#         form_data = aiohttp.FormData()
#         form_data.add_field('contents', 
#                             value="dfdfgd", 
#                             content_type='multipart/form-data')
#         # form_data.add_field('contents', 
#         #                     value=aiohttp.JsonPayload(text_data), 
#         #                     content_type='multipart/form-data')

#         async with session.post(f"{url}?key={api_key}", contents=form_data) as response:
#             if response.status == 200:
#                 result = await response.json()
#                 print(result)
#             else:
#                 print(f"Error: {response.status} - {await response.text()}")

# # Запуск асинхронной функции
# if __name__ == "__main__":
#     asyncio.run(generate_content())


















# async def generate_content():
#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
#     api_key = api_key_gemini
    
#     # Подготовка текстовой части запроса
#     text_data = {
#         "contents": [{
#             "parts": [{"text": "Write a story about a magic backpack."}]
#         }]
#     }

#     # Подготовка файла изображения
#     image_path = './uploads/image.jpg'  # Укажите путь к вашему изображению

#     async with aiohttp.ClientSession() as session:
#         with open(image_path, 'rb') as image_file:
#             form_data = aiohttp.FormData()
#             form_data.add_field('json', 
#                                 value=str(text_data), 
#                                 content_type='application/json')
#             form_data.add_field('file', 
#                                 image_file, 
#                                 filename=image_path,
#                                 content_type='image/jpeg')

#             async with session.post(f"{url}?key={api_key}", data=form_data) as response:
#                 if response.status == 200:
#                     result = await response.json()
#                     print(result)
#                 else:
#                     print(f"Error: {response.status} - {await response.text()}")

# # Запуск асинхронной функции
# if __name__ == "__main__":
#     asyncio.run(generate_content())











































# # Base
# import logging
# import aiohttp
# import asyncio
# # Google
# import google.generativeai as genai
# # Service
# from keys import api_key_gemini, is_admin
# from general_functions import calculation


# genai.configure(api_key=api_key_gemini)


# # Main Text Google Function
# async def mod_gemini(description, image_path):

#     try:
#         username = description.get("username")
#         user_content = description.get("user_content")
#         system_content = description.get("system_content")
#         model_name = description.get("model")
#         # tools = description.get("tools")

#         if not image_path:

#             model = genai.GenerativeModel(
#                 model_name = model_name,
#                 # tools = user_input.tools or None, # "tools": "code_execution",
#                 system_instruction = system_content or None
#             )

#         # if image_path:
#         #     # Getting the base64 string
#         #     base64_file = await encode_image(image_path)

#         response = model.generate_content(user_content)

#         # Tokens:
#         if response:
#             usage_metadata = response.usage_metadata
#             total_token_count = usage_metadata.total_token_count
#             logging.info(f"Gemini text in tokens: {str(model.count_tokens(user_content))}")
#             logging.info(f"Gemini all text tokens: {str(response.usage_metadata)}")
#         else:
#             logging.error("No response from Google Gemini.")
#             return {"response": "No response from Google Gemini."}
        
#         model_version = model_name
#         used_tokens = total_token_count


#         # Calculation of money spent on tokens
#         expenses = await calculation(username, model_version, used_tokens, input_data="text")

#         return {"response": response.text, "expenses": expenses, "used_tokens": used_tokens}
    
#     except Exception as e:
#        logging.error(f"Error is: {e}")
#        return {"Error:": e} # Ни одну ошибку не показывает тварь!!!




























# import PIL.Image

# model = genai.GenerativeModel("gemini-1.5-flash")
# organ = PIL.Image.open(media / "organ.jpg")
# response = model.generate_content(["Tell me about this instrument", organ])
# print(response.text)





# # Upload the file.
# audio_file = genai.upload_file(path='sample.mp3')

# # Initialize a Gemini model appropriate for your use case.
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# # Create the prompt.
# prompt = "Summarize the speech."

# # Pass the prompt and the audio file to Gemini.
# response = model.generate_content([prompt, audio_file])

# # Print the response.
# print(response.text)



# Maximum file 20mb
# # Initialize a Gemini model appropriate for your use case.
# model = genai.GenerativeModel('models/gemini-1.5-flash')

# # Create the prompt.
# prompt = "Please summarize the audio."

# # Load the samplesmall.mp3 file into a Python Blob object containing the audio
# # file's bytes and then pass the prompt and the audio to Gemini.
# response = model.generate_content([
#     prompt,
#     {
#         "mime_type": "audio/mp3",
#         "data": pathlib.Path('samplesmall.mp3').read_bytes()
#     }
# ])

# # Output Gemini's response to the prompt and the inline audio.
# print(response.text)





# # Initialize a Gemini model appropriate for your use case.
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# # Create the prompt.
# prompt = "Generate a transcript of the speech."

# # Pass the prompt and the audio file to Gemini.
# response = model.generate_content([prompt, audio_file])

# # Print the transcript.
# print(response.text)




# # Set the `response_mime_type` to output JSON
# generation_config={"response_mime_type": "application/json"})=

