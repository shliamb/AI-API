# Base
import logging
import asyncio
import re
import base64
import requests
import json
# import datetime
# OpenAI
from openai import AsyncOpenAI, RateLimitError, OpenAIError
from keys import api_key_openai
# Service
from general_functions import calculation


client = AsyncOpenAI(api_key=api_key_openai)







# Function to encode the image
async def encode_image(file_path):
  with open(file_path, "rb") as file_path:
    return base64.b64encode(file_path.read()).decode('utf-8')

# Main OpenAI Function
async def mod_openai_text_img(description, image_path):



    username = description.get("username")
    user_content = description.get("user_content")
    system_content = description.get("system_content", "Ты личный помошник, с отличным чувством юмора")
    model_name = description.get("model")


    try:
        # 1. From the picture
        if image_path:
            # Getting the base64 string
            base64_file = await encode_image(image_path)

            response = await client.chat.completions.create(
            model=model_name,
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_content},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_file}",
                    },
                    },
                ],
                }
            ],
            #max_tokens=300,
            )

        # 2. Without a picture
        if not image_path:
            response = await client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content},
                    ],
                    model=model_name,
            )

        # TOKENS:
        if response:
            response_content = response.choices[0].message.content
            model_version = response.model
            used_tokens = response.usage.total_tokens + response.usage.prompt_tokens
        else:
            logging.error("No response from openai")
            raise
        
        # Calculation of money spent on tokens
        expenses = await calculation(username, model_version, used_tokens, input_data="text")

        return {"response": response_content, "expenses": expenses, "used_tokens": used_tokens}
    



    except RateLimitError as e:
        no_money_openai = ""
        error_message = str(e)
        error_code_match = re.search(r"Error code: (\d+)", error_message)
        error_code = error_code_match.group(1) if error_code_match else "No code provided"
        if error_code == '429':
           no_money_openai = "Error: There is no money for OpenAI account."
           logging.error(f"Error {error_code}: {error_message}, There are not enough funds for OpenAI. Administrators are notified automatically. We will restore everything in the near future.") 
        else:
           no_money_openai = error_message
        return no_money_openai


    except OpenAIError as e:
        # Обработка других ошибок OpenAI
        error_message = str(e)
        logging.error(f"Error: {error_message}")
        return error_message
    


















        #     #OPENAI:
        # chat_completion = await client.chat.completions.create(
        #     messages=[
        #         {"role": "system", "content": user_input.system_content}, # Определение роли AI
        #         {"role": "user", "content": user_input.user_content}, # Сообщение от пользователя для AI
        #         ],
        #         model=user_input.model,
        # )



        # with open(image_path, 'rb') as img_file:
        #     files = {'image': img_file}




        # messages = [
        #     {"role": "system", "content": user_input.system_content},
        #     {"role": "user", "content": user_input.user_content},
        # ]

        # Проверка наличия изображения
        # if image_path:
        #     # Getting the base64 string
        #     base64_image = await encode_image(image_path)
        #     messages.append({"image_url": "user", "url": f"data:image/jpeg;base64,{base64_image}"})

        # chat_completion = await client.chat.completions.create(
        #     messages=messages,
        #     model=user_input.model,
        # )