from pathlib import Path
from openai import AsyncOpenAI, RateLimitError, OpenAIError
# import aiofiles

from keys import API_KEY_OPENAI

import aiofiles
import httpx
import asyncio
import io
import requests

import aiohttp
from general_functions import encode_file


from aiohttp import ClientSession, FormData

# client = AsyncOpenAI(api_key=API_KEY_OPENAI)


# async def transcription_openai(description, audio_path):

#     username = description.get("username")
#     prompt = description.get("prompt")
#     language = description.get("language") # input language in ISO-639-1, will improve accuracy and latency - ru or en
#     model = description.get("model", "whisper-1") # whisper-1 only now
#     response_format = description.get("response_format", "text") # json, text, srt, verbose_json, or vtt

#     # async with aiofiles.open(audio_path, "rb") as file:

#         #content = file._file

#     encoded_audio = await encode_file(audio_path)

#     transcript = await client.audio.transcriptions.create(
#         model = model,
#         prompt = prompt,
#         language = language,
#         response_format = response_format,
#         # timestamp_granularities=["word"],
#         # timestamp_granularities=["segment"]
#         file = encoded_audio
#     )

#     return transcript








async def transcription_openai(description, audio_file_path):
    username = description.get("username")
    prompt = description.get("prompt")
    language = description.get("language")  # input language in ISO-639-1
    model = description.get("model", "whisper-1")  # whisper-1 only now
    response_format = description.get("response_format", "text")  # json or text

    url = "https://api.openai.com/v1/audio/transcriptions"

    headers = {
        "Authorization": f"Bearer {API_KEY_OPENAI}",
        # "Content-Type": "multipart/form-data",
    }


    async with ClientSession() as session:
        async with aiofiles.open(audio_file_path, 'rb') as audio_file:

            # Создаем объект FormData
            form = FormData()

            # file_data = await audio_file.read()
            file_data = audio_file._file
            
            # # Добавляем файлы в FormData
            # for file_key, file_value in file_data.items():
            #     form.add_field(file_key, file_value['content'], filename=file_value['filename'])

            # Добавляем дополнительные данные в FormData
            form.add_field('file', file_data)
            form.add_field('model', model)
            # form.add_field('language', language)
            # form.add_field('prompt', prompt)
            # form.add_field('response_format', response_format)


            async with session.post(url, headers=headers, data=form) as response:
                #response_data = await response.json()
                if response.status == 200:
                    #return {"response": await response.text()}
                    print(await response.text())
                else:
                    print("Error:", response.status, await response.text())



            # Отправляем POST запрос с использованием FormData
            # async with session.post(url, headers=headers, data=form) as response:
            #     response_data = await response.json()
            # data = {
            #     "model": model,
            #     "language": language,
            #     "prompt": prompt,
            #     "response_format": response_format,
            # }

            # Отправляем POST запрос с использованием FormData
            # async with session.post(url, headers=headers, data=form) as response:
            #     response_data = await response.json()

        # async with aiohttp.ClientSession() as session:
        #     async with aiofiles.open(audio_file_path, 'rb') as audio_file: 
        #         file_data = await audio_file.read()
                
        #         data = {
        #             "model": model,
        #             "language": language,
        #             "prompt": prompt,
        #             "response_format": response_format,
        #         }
                



    #             if response.status == 200:
    #                 #return {"response": await response.text()}
    #                 print(await response.text())
    #             else:
    #                 print("Error:", response.status, await response.text())






# async with ClientSession() as session:
#     # Создаем объект FormData
#     form = FormData()
    
#     # Добавляем файлы в FormData
#     for file_key, file_value in file_data.items():
#         form.add_field(file_key, file_value['content'], filename=file_value['filename'])

#     # Отправляем POST запрос с использованием FormData
#     async with session.post(url, headers=headers, data=form) as response:
#         response_data = await response.json()

















# async def transcription_openai(description, audio_file_path):
#     username = description.get("username")
#     prompt = description.get("prompt")
#     language = description.get("language")  # input language in ISO-639-1, will improve accuracy and latency - ru or en
#     model = description.get("model", "whisper-1")  # whisper-1 only now
#     response_format = description.get("response_format", "text")  # json, text, srt, verbose_json, or vtt

#     url = "https://api.openai.com/v1/audio/transcriptions"

#     headers = {
#         "Authorization": f"Bearer {API_KEY_OPENAI}",
#     }

#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, headers=headers, data={
#             "model": model,
#             "language": language,
#             "prompt": prompt,
#             "response_format": response_format,
#         }, files={'files': open(audio_file_path, 'rb')}) as response:
#             if response.status == 200:
#                 return {"response": await response.text()}
#             else:
#                 print("Error:", response.status, await response.text())

# # Пример вызова функции
# # asyncio.run(transcription_openai(description, audio_file_path))










# async def transcription_openai(description, audio_file_path):

#     username = description.get("username")
#     prompt = description.get("prompt")
#     language = description.get("language") # input language in ISO-639-1, will improve accuracy and latency - ru or en
#     model = description.get("model", "whisper-1") # whisper-1 only now
#     response_format = description.get("response_format", "text") # json, text, srt, verbose_json, or vtt

#     url = "https://api.openai.com/v1/audio/transcriptions"
    
#     headers = {
#         "Authorization": f"Bearer {API_KEY_OPENAI}",
#     }

#     with open(audio_file_path, 'rb') as audio_file: # Открываем файл в бинарном режиме

#         files = {
#             'file': audio_file,
#         }

#         data = {
#             "model": model,
#             "language": language,
#             "prompt": prompt,
#             "response_format": response_format,
#         }

#         response = requests.post(url, headers=headers, files=files, data=data)

#         if response.status_code == 200:
#             return {"response": response.text}
#         else:
#             print("Error:", response.status_code, response.text)











    # async with aiohttp.ClientSession() as session:

    #     encoded_audio = await encode_file(audio_file_path)

    #     # Формируем JSON-объект
    #     payload = {
    #         "inline_data": {
    #             "mime_type": "audio/ogg",  # audio/ogg  audio/mpeg или другой подходящий тип для вашего аудио
    #             "data": encoded_audio  # переменная с закодированными данными аудиофайла
    #         },
    #         # "system_instruction": {
    #         #     "parts": {
    #         #         "text": system_content
    #         #     }
    #         # },
    #         "model": model,
    #     }


    #     async with session.post(url, headers=headers, json=payload) as response:
    #         result = await response.json()
    #         return result



# if __name__ == "__main__":
#     asyncio.run(transcription_openai())




# async with aiohttp.ClientSession() as session:
#     with open(audio_path, 'rb') as f:
#         data = {
#             'file': f  # Здесь 'file' - это имя поля формы
#         }
#         async with session.post(url, headers=headers, data=data) as response:
#             result = await response.json()


# # Закрытие файла после запроса
# files['file'].close()


























# client = AsyncOpenAI(api_key=API_KEY_OPENAI)


# async def transcription_openai(description, audio_path):

#     username = description.get("username")
#     prompt = description.get("prompt")
#     language = description.get("language") # input language in ISO-639-1, will improve accuracy and latency - ru or en
#     model = description.get("model", "whisper-1") # whisper-1 only now
#     response_format = description.get("response_format", "text") # json, text, srt, verbose_json, or vtt

#     async with aiofiles.open(audio_path, "rb") as file:

#         content = file._file

#         transcript = await client.audio.transcriptions.create(
#             model = model,
#             prompt = prompt,
#             language = language,
#             response_format = response_format,
#             # timestamp_granularities=["word"],
#             # timestamp_granularities=["segment"]
#             file = content
#         )

#     return transcript




        # content = await file.read()
        # file_like_object = io.BytesIO(content)





# async def transcription_openai(description, audio_file_path):

#     username = description.get("username")
#     prompt = description.get("prompt")
#     language = description.get("language") # input language in ISO-639-1, will improve accuracy and latency - ru or en
#     model = description.get("model", "whisper-1") # whisper-1 only now
#     response_format = description.get("response_format", "text") # json, text, srt, verbose_json, or vtt

#     url = "https://api.openai.com/v1/audio/transcriptions"
    
#     async with httpx.AsyncClient() as client:
#         async with aiofiles.open(audio_file_path, 'rb') as audio_file:
#             # Читаем файл асинхронно
#             file_content = await audio_file.read()
            
#             # Подготовка данных для отправки
#             files = {
#                 'file': ('in_audio.ogg', file_content),
#                 'model': (None, model)
#             }
            
#             headers = {
#                 "Authorization": f"Bearer {api_key_openai}",
#                 "Content-Type": "multipart/form-data"
#             }

#             # Выполнение POST-запроса
#             response = await client.post(url, headers=headers, files=files)
            
#             # Обработка ответа
#             if response.status_code == 200:
#                 return response.json()
#             else:
#                 raise Exception(f"Error {response.status_code}: {response.text}")

# # Пример использования
# if __name__ == "__main__":
#     # OPENAI_API_KEY = api_key_openai
#     # AUDIO_FILE_PATH = "/path/to/file/audio.mp3"

#     asyncio.run(transcription_openai())









# async with aiofiles.open(audio_path, "rb") as file:
#     content = await file.read()  # Читаем содержимое файла


# async def read_file_async(audio_path):
#     async with aiofiles.open(audio_path, 'rb') as file:
#         content = await file.read()
#     return content

# content = await read_file_async(audio_path)
