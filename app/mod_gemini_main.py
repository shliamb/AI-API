# https://github.com/google-gemini/generative-ai-python/blob/main/google/generativeai/answer.py

# Base
import logging
# import aiohttp
# import asyncio
# Google
import google.generativeai as genai
import PIL.Image
# Service
from keys import api_key_gemini, is_admin
from general_functions import calculation


genai.configure(api_key=api_key_gemini)


# Main Text Google Function
async def mod_gemini(description, image_path):

    try:
        username = description.get("username")
        user_content = description.get("user_content")
        system_content = description.get("system_content")
        model_name = description.get("model")
        # tools = description.get("tools")


        model = genai.GenerativeModel(
            model_name = model_name,
            # tools = user_input.tools or None, # "tools": "code_execution",
            system_instruction = system_content or None
        )

        if not image_path:
            response = model.generate_content(user_content)

        if image_path:
            organ = PIL.Image.open(image_path)
            response = model.generate_content([user_content, organ])

        # Tokens:
        if response:
            usage_metadata = response.usage_metadata
            total_token_count = usage_metadata.total_token_count
            logging.info(f"Gemini text in tokens: {str(model.count_tokens(user_content))}")
            logging.info(f"Gemini all text tokens: {str(response.usage_metadata)}")
        else:
            logging.error("No response from Google Gemini.")
            return {"response": "No response from Google Gemini."}
        
        model_version = model_name
        used_tokens = total_token_count


        # Calculation of money spent on tokens
        expenses = await calculation(username, model_version, used_tokens, input_data="text")

        return {"response": response.text, "expenses": expenses, "used_tokens": used_tokens}
    
    except Exception as e:
       logging.error(f"Error is: {e}")
       return {"Error:": e} # Ни одну ошибку не показывает тварь!!!







































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

