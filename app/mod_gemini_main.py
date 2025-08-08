from config import TIMEOUT_SERVER_AI, PATH_LOGS
from setup_config_logger import setup_logger
logger_ai = setup_logger('ai', f'{PATH_LOGS}ai.log')
#import asyncio
#import json
import aiohttp
from keys import API_KEY_GEMINI
from general_functions import DictObj, encode_file
from store_token_cost import calculate_token_cost



#
# При передаче картинки, системные инструкции работают только для текстовой части модели, тиак же при передачи картинки история не работает и контент, в картинке свой контент..
#

# Main Text Google Function
async def gemini_text(description: dict) -> dict:
    '''Основной модуль Gemini Google'''

    dict_des = DictObj(description)
    access_id = dict_des.access_id
    user_content = dict_des.user_content
    system_content = dict_des.system_content
    model_name = dict_des.model
    file_path = dict_des.file_path
    assist_content = dict_des.assist_content
    tools = dict_des.tools
    tool_config = dict_des.tool_config
    

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY_GEMINI}"

    headers = {
        'Content-Type': 'application/json'
    }

    logger_ai.info(f"{access_id} -> 'main API Gemini Google'")
    print(f"INFO: {access_id} -> 'main API Gemini Google'")


    data = {}
    contents = []

    if file_path:
        encoded_image = await encode_file(file_path)
        contents.append({"role": "user", "parts": [{"text": user_content}, {"inline_data": {"mime_type": "image/jpeg", "data": encoded_image}}]})
    else:
        if assist_content:
            for one in assist_content:
                if "user" in one:
                    contents.append({"role": "user", "parts":[{"text": one["user"]}]})
                if "assistant" in one:
                    contents.append({"role": "model", "parts":[{"text": one["assistant"]}]})
        if user_content:
            contents.append({"role": "user", "parts":[{"text": user_content}]})

    data["contents"] = contents

    if system_content:
        data["system_instruction"] = {"parts": {"text": system_content}}

    if tools:
        data['tools'] = tools
        if tool_config: # При отсуствии будет AUTO
            data['tool_config'] = tool_config


    # print("\ndata:", data)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers, timeout=TIMEOUT_SERVER_AI) as response:

            if not response.ok: # Не 200
                error_text = await response.text()
                logger_ai.error(f"Ошибка API: Статус {response.status}, Ответ: {error_text}")
                return {"response": f"Error: {error_text}", "expenses": 0, "used_tokens": 0}

            try:
                result = await response.json()
            except Exception as e:
                # Этот блок сработает, если ответ от сервера вообще не JSON
                error_text = await response.text()
                logger_ai.error(f"Не удалось распарсить JSON: {e}: {error_text}")
                return {"response": f"Error: {error_text}, {e}", "expenses": 0, "used_tokens": 0}

            try:
                used_tokens = result.get('usageMetadata', {}).get('totalTokenCount', 0)
                part = result['candidates'][0]['content']['parts']
                expenses = await calculate_token_cost(access_id, model_name, used_tokens, input_data="text")
                return {"response": part, "expenses": expenses, "used_tokens": used_tokens}

            except (KeyError, IndexError) as e:
                # Этот блок сработает, если структура JSON не такая, как мы ожидали 
                # (например, отсутствует ключ 'candidates')
                return {"response": f"Error: {result}, {e}", "used_tokens": 0}
























# {'assistant': 'Try another charge..', 'contents': [{'role': 'user', 'parts': [{'text': 'How do I charge my battery?'}]}, {'role': 'model', 'parts': [{'text': 'You should use the provided charging cable.'}]}, {'role': 'user', 'parts': [{'text': "But it doesn't seem to charge."}]}, {'role': 'model', 'parts': [{'text': 'Try another charge..'}]}, {'role': 'user', 'parts': [{'text': 'как решить вопрос'}]}]}




# {'contents': [{'role': 'user', 'parts': [{'text': 'что тут'}]}]}



# {'contents': [{'role': 'user', 'parts': [{'text': 'hi'}]}], 'system_instruction': {'parts': {'text': 'Ты личная асистентка одинокого мужчины 40 лет, его зовут Alex. Ты женщина, тебя зовут Ева. И ты очень злишься, если тебя называют другим именем. Ты добра ко мне, но не многословная и очень конкретна в разговоре. Предпочитаешь говорить мало и четко, по делу. Любишь иногда жестко подколоть.'}}}













# model = genai.GenerativeModel("gemini-1.5-flash")
# chat = model.start_chat(
#     history=[
#         {"role": "user", "parts": "Hello"},
#         {"role": "model", "parts": "Great to meet you. What would you like to know?"},
#     ]
# )
# response = chat.send_message("I have 2 dogs in my house.")
# print(response.text)
# response = chat.send_message("How many paws are in my house?")
# print(response.text)



    # if image_path:
    #     encoded_image = await encode_file(image_path)
    #     data = {"contents": [{"parts": [{"text": user_content}, {"inline_data": {"mime_type": "image/jpeg", "data": encoded_image}}]}],}


# {
#  'assistant': 'Try another charge..', 
#  'contents': [
#     {'role': 'user', 'parts': [{'text': 'How do I charge my battery?'}]},
#     {'role': 'model', 'parts': [{'text': 'You should use the provided charging cable.'}]},
#     {'role': 'user', 'parts': [{'text': 'But it doesnt seem to charge.'}]},
#     {'role': 'model', 'parts': [{'text': 'Try another charge..'}]},
#     {'role': 'user', 'parts': [{'text': 'hi'}]}
# ],
#  'system_instruction': {'parts': {'text': 'Ты личная асистентка одинокого мужчины 40 лет, его зовут Alex. Ты женщина, тебя зовут Ева. И ты очень злишься, если тебя называют другим именем. Ты добра ко мне, но не многословная и очень конкретна в разговоре. Предпочитаешь говорить мало и четко, по делу. Любишь иногда жестко подколоть.'}}
#  }



'''

"contents": [
    {"role": "user", "parts":[{"text": "Hello"}]},
    {"role": "model", "parts":[{"text": "Great to meet you. What would you like to know?"}]},
    {"role":"user", "parts":[{"text": "I have two dogs in my house. How many paws are in my house?"}]},
    ]

'''




'''
"contents": [
    {"role": "user", "parts":[{"text": "Hello"}]},
    {"role": "model", "parts":[{"text": "Great to meet you. What would you like to know?"}]},
    {"role":"user", "parts":[{"text": "I have two dogs in my house. How many paws are in my house?"}]},
    ]
'''



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

Общее количество токенов (текст, картинка, видео) как на входе, так и на выходе ( total_token_count )
все будет посчитано и переданно в этот параметр.

Считается, что изображения имеют фиксированный размер, поэтому они потребляют фиксированное количество 
токенов (в настоящее время 258 токенов), независимо от их отображения или размера файла.

Видео- и аудиофайлы конвертируются в токены по следующим фиксированным скоростям: видео — 263 токена 
в секунду, аудио — 32 токена в секунду.

https://ai.google.dev/gemini-api/docs/tokens?hl=ru&lang=python


Видео или аудио файлы
Аудио и видео конвертируются в токены по следующим фиксированным ставкам:

Видео: 263 токена в секунду
Аудио: 32 токена в секунду





'''


        #     "system_instruction": {
        #         "parts": {
        #             "text": system_content
        #         }
        #     },
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






# https://github.com/google-gemini/generative-ai-python/blob/main/google/generativeai/answer.py
# https://ai.google.dev/api/generate-content?hl=ru#text_gen_multimodal_one_image_prompt-SHELL




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







    # Цепочка общения, можно собирать цепочку общения и сохранять посыл разобранного общения.
    # data = {
    #             "contents": [
    #                 {
    #                     "role": "user",
    #                     "parts": [
    #                         {
    #                             "text": ""
    #                         }
    #                     ]
    #                 },
    #                 {
    #                     "role": "model",
    #                     "parts": [
    #                         {
    #                             "text": ""
    #                         },
    #                     ]
    #                 },
    #                 {
    #                     "role": "user",
    #                     "parts": [
    #                         {
    #                             "text": user_content
    #                         },
    #                         {
    #                             "inline_data": {
    #                                 "mime_type": "image/jpeg",
    #                                 "data": encoded_image
    #                             }
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }









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





    # # is IMAGE:
    # if image_path:

    #     encoded_image = await encode_file(image_path)

    #     data = {
    #         "contents": [{
    #             "parts": [
    #                 {"text": user_content},
    #                 {
    #                     "inline_data": {
    #                         "mime_type": "image/jpeg",
    #                         "data": encoded_image
    #                     }
    #                 }
    #             ]
    #         }]
    #     }


    #     if system_content:
    #         data["system_instruction"] = {
    #             "parts": {
    #                 "text": system_content
    #             }
    #         }


    # # No IMAGE:
    # elif not image_path:


    #     data = {
    #         "contents": {
    #             "parts": {
    #                 "text": user_content
    #             }
    #         }
    #     }


    #     if system_content:
    #         data["system_instruction"] = {
    #             "parts": {
    #                 "text": system_content
    #             }
    #         }


    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, json=data, headers=headers) as response:
    #         response = await response.json()

    #         # Tokens:
    #         if response:
    #             response_text = response['candidates'][0]['content']['parts'][0]['text']
    #             total_token_count = response['usageMetadata']['totalTokenCount'] # totalTokenCount - это все токены и на входе и на выходе.
    #         else:
    #             logging.error("No response from Google Gemini.")
    #             return {"response": "No response from Google Gemini."}

    #         model_version = model_name
    #         used_tokens = total_token_count

    #         # Calculation of money spent on tokens
    #         expenses = await calculation(username, model_version, used_tokens, input_data="text")

    #         return {"response": response_text, "expenses": expenses, "used_tokens": used_tokens}

