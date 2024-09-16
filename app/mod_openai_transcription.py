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






async def transcription_openai(description, audio_file_path):

    username = description.get("username")
    prompt = description.get("prompt")
    language = description.get("language") # input language in ISO-639-1, will improve accuracy and latency - ru or en
    model = description.get("model", "whisper-1") # whisper-1 only now
    response_format = description.get("response_format", "text") # json, text, srt, verbose_json, or vtt

    url = "https://api.openai.com/v1/audio/transcriptions"
    

    headers = {
        "Authorization": f"Bearer {API_KEY_OPENAI}",
    }

    async with aiohttp.ClientSession() as session:

        encoded_image = await encode_file(audio_file_path)

        #with open(audio_file_path, 'rb') as f:
        data = aiohttp.FormData()
        data.add_field('file', encoded_image)
        #data.add_field('model', model)

        async with session.post(url, headers=headers, data=data) as response:
            result = await response.json()
            return result



if __name__ == "__main__":
    asyncio.run(transcription_openai())




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
