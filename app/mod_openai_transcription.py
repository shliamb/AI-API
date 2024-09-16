from openai import AsyncOpenAI, RateLimitError, OpenAIError
from keys import API_KEY_OPENAI
import aiofiles
from general_functions import read_audio_file, calculation

client = AsyncOpenAI(api_key=API_KEY_OPENAI)

async def transcription_openai(description, audio_path):

    username = description.get("username")
    prompt = description.get("prompt")
    language = description.get("language") # input language in ISO-639-1, will improve accuracy and latency - ru or en
    model = description.get("model", "whisper-1") # whisper-1 only now
    response_format = description.get("response_format", "text") # json, text, srt, verbose_json, or vtt

    # with open(audio_path, "rb") as file:
    audio_file = open(audio_path, "rb")

    transcript = await client.audio.transcriptions.create(
        file = audio_file,
        model = model,
        prompt = prompt,
        language = language,
        response_format = response_format,
    )

        #length_of_audio = await read_audio_file(audio_path) # mp3 (ID3v1 и ID3v2), flac, ogg Vorbis, acc (and M4A), wav, wma (limited support), aiff

        # Statistic
        #used_tokens = length_of_audio
        #model_version = model # just only whisper-1
        
        # Calculation of money spent on minutes + sec
        #expenses = await calculation(username, model_version, used_tokens, input_data="audio")

    print(transcript.words)
    return {"response": transcript}#, "expenses": expenses, "minutes": length_of_audio}






'''
Suport files Mutagen:

  - MP3 (ID3v1 и ID3v2)
  - FLAC
  - Ogg Vorbis
  - AAC (включая M4A)
  - WAV
  - WMA (ограниченная поддержка)
  - AIFF

'''
































# async def transcription_openai(description, audio_file_path):
#     username = description.get("username")
#     prompt = description.get("prompt")
#     language = description.get("language")  # input language in ISO-639-1
#     model = description.get("model", "whisper-1")  # whisper-1 only now
#     response_format = description.get("response_format", "text")  # json or text

#     url = "https://api.openai.com/v1/audio/transcriptions"

#     headers = {
#         "Authorization": f"Bearer {API_KEY_OPENAI}",
#     }


#     async with ClientSession() as session:
#         async with aiofiles.open(audio_file_path, 'rb') as audio_file:

#             # Создаем объект FormData
#             form = FormData()

#             # file_data = await audio_file.read() - не работае, хотя и асинхронный, он открывает фал и отдает чисто данные асинхронно, но так опенаи не принимает
#             # file_data = audio_file._file - работает но не асинхронный вариант

#             # Добавляем дополнительные данные в FormData
#             form.add_field('file', file_data)
#             form.add_field('model', model)
#             # form.add_field('language', language)
#             # form.add_field('prompt', prompt)
#             # form.add_field('response_format', response_format)

#             async with session.post(url, headers=headers, data=form) as response:
#                 #response_data = await response.json()
#                 if response.status == 200:
#                     #return {"response": await response.text()}
#                     print(await response.text())
#                 else:
#                     print("Error:", response.status, await response.text())




















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
