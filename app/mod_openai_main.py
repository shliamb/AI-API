# Base
import logging
import re
# OpenAI
from openai import AsyncOpenAI, RateLimitError, OpenAIError
from keys import API_KEY_OPENAI
# Service
from general_functions import calculation, encode_file
from config import defoult_model_openai


client = AsyncOpenAI(api_key=API_KEY_OPENAI)



#
# При передаче картинки, системные инструкции работают только для текстовой части модели, тиак же при передачи картинки история не работает и контент, в картинке свой контент..
#
# Main Text OpenAI Function .
async def mod_openai_text_img(description, image_path):

    username = description.get("username")
    user_content = description.get("user_content")
    system_content = description.get("system_content")
    model_name = description.get("model", defoult_model_openai)
    assist_content = description.get("assist_content")
    response_format = description.get("response_format")


    response = await client.responses.create(
        model="gpt-4o", input="Explain disestablishmentarianism to a smart five year old."
    )
    print(response.output_text)

    # try:

    #     messages_ai = []

    #     if system_content: # if system_content and model_name not in ("o1-preview", "o1-mini", "o1", "o3-mini"):
    #         messages_ai.append({"role": "system", "content": system_content},)

    #     if image_path:
    #         base64_file = await encode_file(image_path)
    #         messages_ai.append({"role": "user", "content": [{"type": "text", "text": user_content}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_file}",},},],},)
    #     else:
    #         if assist_content:
    #             for data in assist_content:
    #                 if "user" in data:
    #                     messages_ai.append({"role": "user", "content": data["user"]})
    #                 if "assistant" in data:
    #                     messages_ai.append({"role": "assistant", "content": data["assistant"]})
    #         if user_content:
    #             messages_ai.append({"role": "user", "content": user_content},)
    #         if not response_format:
    #             response_format = {"type": "text"}

    #     # OpenAI:
    #     response = await client.responses.create( # client.chat.completions.create(
    #         model = model_name,
    #         input = messages_ai,
    #         response_format = response_format
    #         #instructions = instructions
    #     )

    #     print()
    #     print(response)
    #     print(response.output_text)
    #     print(response.output)

    #     # TOKENS:
    #     try:
    #         response_content = response.output_text #response.choices[0].message.content
    #         model_version = response.model
    #         used_tokens = response.usage.total_tokens + response.usage.prompt_tokens

    #         # Calculation of money spent on tokens
    #         expenses = await calculation(username, model_version, used_tokens, input_data="text")

    #         return {"response": response_content, "expenses": expenses, "used_tokens": used_tokens}

    #     except:
    #         response_content = response.output_text 
    #         return {"response": response_content, "expenses": 0, "used_tokens": 0}
        


    # except RateLimitError as e:
    #     no_money_openai = ""
    #     error_message = str(e)
    #     error_code_match = re.search(r"Error code: (\d+)", error_message)
    #     error_code = error_code_match.group(1) if error_code_match else "No code provided"
    #     if error_code == '429':
    #        no_money_openai = "Error: There is no money for OpenAI account."
    #        logging.error(f"Error {error_code}: {error_message}, There are not enough funds for OpenAI. Administrators are notified automatically. We will restore everything in the near future.") 
    #     else:
    #        no_money_openai = error_message
    #     return no_money_openai


    # except OpenAIError as e:
    #     # Обработка других ошибок OpenAI
    #     error_message = str(e)
    #     logging.error(f"Error: {error_message}")
    #     return error_message
    




'''

Условия API Openai:
https://community.openai.com/c/api/7

messages: !

1. Request body:
{"role": "system", "name": "RoboCop", "content": ..
{"role": "user", "name": "Alex", "content": "Hello!"}
        image_url 
            url
            detail..

Массив частей содержимого с определенным типом, каждая из которых 
может иметь тип text или image_url при передаче изображений. Вы 
можете передать несколько изображений, добавив несколько частей 
содержимого image_url. Ввод изображений поддерживается только при 
использовании модели gpt-4o.

2. Assistant message:
leter..

3. Tool message:
leter..

4. max_tokens integer или null Необязательно 
Максимальное количество лексем, которые могут быть сгенерированы 
в завершении чата. Общая длина входных и сгенерированных лексем 
ограничена длиной контекста модели. Пример Python-кода для подсчета 
токенов.

... 
Там очень много всего, я хз.






'''



            # messages=[
            #     {
            #     "role": "user",
            #     "content": [
            #         {"type": "text", "text": user_content},
            #         {
            #         "type": "image_url",
            #         "image_url": {
            #             "url": f"data:image/jpeg;base64,{base64_file}",  # Так можно накидать много картинок, хз хз за чем..
            #         },
            #         },
            #     ],
            #     }
            # ],
            # )











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