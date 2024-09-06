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
from general_functions import day_utcnow, unformat_date, calculation
from config import price, time_correction
from worker_db import add_statistic, get_user_by_username, update_user_by_username

client = AsyncOpenAI(api_key=api_key_openai)







# Function to encode the image
async def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Main OpenAI Function
async def mod_openai(username, user_input, image_path):

    try:

        if image_path is not None:
            # Getting the base64 string
            base64_image = await encode_image(image_path)
            image_message = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        else:
            image_message = ""



        # Формируем список сообщений
        # messages = [{"role": "user", "content": {"type": "text", "text": user_input.system_content}}]

        # # Добавляем сообщение с картинкой, если оно существует
        # if image_message:
        #     messages[0]["content"].append(image_message)

        # # Добавляем основное сообщение пользователя
        # messages.append({"role": "user", "content": user_input.user_content})

        # chat_completion = await client.chat.completions.create(
        #     model="gpt-4o",
        #     messages=messages,
        #     max_tokens=300  # Ограничиваем лимит ответа в токенах
        # )



        chat_completion = await client.chat.completions.create(
            model="gpt-4o",
            messages = [
                        {"role": "user", "content": [
                                                        {"type": "text", "text": user_input.system_content},
                                                        #{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}",}},
                                                    ],
                        },
                        {"role": "user", "content": user_input.user_content},
                        ],
                        max_tokens=300, # Ограничевает лимит ответа в токенах
        )




        # TOKENS:
        # Извлечение ответа статистики из результата
        if chat_completion:
            response_content = chat_completion.choices[0].message.content
            model_version = chat_completion.model
            prompt_tokens = chat_completion.usage.prompt_tokens
            used_tokens = chat_completion.usage.total_tokens + prompt_tokens
        else:
            logging.error("No response from openai")
            raise
        
        # # Расчет потраченых денег на токены
        # data = await calculation(price, model_version, used_tokens)

        # # STATISTIC:
        # # Сбор данных
        # data_stat = {
        #     "username_table_stat": username,
        #     "time": await day_utcnow(time_correction),
        #     "use_model": model_version,
        #     "sesion_token": data[1],
        #     "price_1_tok": data[0],
        #     "total_price": data[2],
        # }

        # # SAVE STATISTIC TO DB:
        # await add_statistic(data_stat)
        # # Получаю данные пользователя
        # user_data = await get_user_by_username(username)
        # new_money = user_data.money - data[2]
        # data_money = {"money": new_money}
        # # Баланс изменили с учетом расхода
        # await update_user_by_username(username, data_money)

        return {"response": response_content}
    



    except RateLimitError as e:
        no_money_openai = 0
        error_message = str(e)
        error_code_match = re.search(r"Error code: (\d+)", error_message)
        error_code = error_code_match.group(1) if error_code_match else "No code provided"
        if error_code == '429':
           logging.error(f"Error {error_code}: {error_message}, There are not enough funds for OpenAI. Administrators are notified automatically. We will restore everything in the near future.") 
        no_money_openai = "Error: There is no money for OpenAI account."
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