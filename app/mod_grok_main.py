from config import TIMEOUT_SERVER_AI
from setup_config_logger import setup_logger
logger_ai = setup_logger('ai', '/log/ai.log')
#import asyncio
import aiohttp
#import json
from keys import API_KEY_GROK
from general_functions import DictObj, encode_file
from store_token_cost import calculate_token_cost




# Main Text GROK Function
async def grok_text(description: dict) -> dict:
    '''Основной модуль GROK'''

    dict_des = DictObj(description)
    access_id = dict_des.access_id
    user_content = dict_des.user_content
    system_content = dict_des.system_content
    model_name = dict_des.model
    assist_content = dict_des.assist_content
    file_path = dict_des.file_path
    # tools = description.get("tools")
    # ?? 'response_format':'[generationConfig: {responseMimeType: "application/json",responseSchema: {type: SchemaType.ARRAY,items: {type: SchemaType.OBJECT,properties: {recipe_name: {type: SchemaType.STRING,},},},},}});]'

    logger_ai.info(f"{access_id} -> 'main API GROK'")
    print(f"INFO: {access_id} -> 'main API GROK'")


    file_path = None # Пока не нашел как передавать картинкун

    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY_GROK}"
    }

    data = {}
    contents = []

    if file_path: # ? 
        encoded_image = await encode_file(file_path)
        contents.append({"role": "user", "content": [
            {
                "type": "image",
                "source": {
                "type": "base64",
                "media_type": "image/jpeg", # image/jpeg, image/png, image/gif, and image/webp
                "data": encoded_image,
                }
            },
            {"type": "text", "text": user_content}
        ]})

    else:
        if assist_content:
            for one in assist_content:
                if "user" in one:
                    contents.append({"role": "user", "content": one["user"]})
                if "assistant" in one:
                    contents.append({"role": "assistant", "content":one["assistant"]})
        if user_content:
            contents.append({"role": "user", "content": user_content})
        if system_content:
            contents.append({"role": "system", "content": system_content})


    data["messages"] = contents
    data["model"] = model_name
    data["stream"] = False
    data["temperature"] = 0


    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers, timeout=TIMEOUT_SERVER_AI) as response:

            try:
                result = await response.json()
            except:
                text_data = await response.text()
                return {"response": text_data, "expenses": 0, "used_tokens": 0}

            # Tokens:
            try:
                response_text = result['choices'][0]['message']['content']
                used_tokens = result['usage']['total_tokens']
            except:
                text_data = await response.text()
                return {"response": text_data, "expenses": 0, "used_tokens": 0}

            # Calculation of money spent on tokens
            expenses = await calculate_token_cost(access_id, model_name, used_tokens, input_data="text")
            return {"response": response_text, "expenses": expenses, "used_tokens": used_tokens}




















# response = {'id': '5c301da4-d584-4296-8967-6f190f3fe3c3', 'object': 'chat.completion', 'created': 1739048859, 'model': 'grok-2-vision-1212', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': 'Привет', 'refusal': None}, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 13, 'completion_tokens': 67, 'total_tokens': 80, 'prompt_tokens_details': {'text_tokens': 13, 'audio_tokens': 0, 'image_tokens': 0, 'cached_tokens': 0}}, 'system_fingerprint': 'fp_21e54090c4'}






    # data = {
    #     "messages": [
    #         {"role": "system", "content": "You are a test assistant."},
    #         {"role": "user", "content": "Testing. Just say hi and hello world and nothing else."}
    #     ],
    #     "model": "grok-2-latest",
    #     "stream": False,
    #     "temperature": 0
    # }







            # content = response['choices'][0]['message']['content']
            # total_tokens = response['usage']['total_tokens']
            # text_tokens = response['usage']['prompt_tokens_details']['text_tokens']
            # audio_tokens = response['usage']['prompt_tokens_details']['audio_tokens']
            # image_tokens = response['usage']['prompt_tokens_details']['image_tokens']
            # cached_tokens = response['usage']['prompt_tokens_details']['cached_tokens']






# from config import LOG_CONFIG_AI, TIMEOUT_SERVER_AI
# import logging
# logging.basicConfig(**LOG_CONFIG_AI)
# import asyncio
# import aiohttp
# from keys import API_KEY_GROK
# from general_functions import DictObj, encode_file
# from store_token_cost import calculate_token_cost




# # Main Text GROK Function
# async def grok_text(description: dict) -> dict:
#     '''Основной модуль GROK'''

#     dict_des = DictObj(description)
#     access_id = dict_des.access_id
#     user_content = dict_des.user_content
#     system_content = dict_des.system_content
#     model_name = dict_des.model
#     assist_content = dict_des.assist_content
#     file_path = dict_des.file_path
#     # tools = description.get("tools")
#     # ?? 'response_format':'[generationConfig: {responseMimeType: "application/json",responseSchema: {type: SchemaType.ARRAY,items: {type: SchemaType.OBJECT,properties: {recipe_name: {type: SchemaType.STRING,},},},},}});]'

#     logging.info(f"{access_id} -> 'main API GROK'")
#     print(f"INFO: {access_id} -> 'main API GROK'")


#     file_path = None # Пока не нашел как передавать картинкун

#     url = "https://api.x.ai/v1/chat/completions"

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {API_KEY_GROK}"
#     }

#     data = {}
#     contents = []

#     if file_path: # ? 
#         encoded_image = await encode_file(file_path)
#         contents.append({"role": "user", "content": [
#             {
#                 "type": "image",
#                 "source": {
#                 "type": "base64",
#                 "media_type": "image/jpeg", # image/jpeg, image/png, image/gif, and image/webp
#                 "data": encoded_image,
#                 }
#             },
#             {"type": "text", "text": user_content}
#         ]})

#     else:
#         if assist_content:
#             for one in assist_content:
#                 if "user" in one:
#                     contents.append({"role": "user", "content": one["user"]})
#                 if "assistant" in one:
#                     contents.append({"role": "assistant", "content":one["assistant"]})
#         if user_content:
#             contents.append({"role": "user", "content": user_content})
#         if system_content:
#             contents.append({"role": "system", "content": system_content})


#     data["messages"] = contents
#     data["model"] = model_name
#     data["stream"] = False
#     data["temperature"] = 0



#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, json=data, headers=headers) as response:
#             try:
#                 response = await response.json()
#                 print(response)

#                 # content = response['choices'][0]['message']['content']
#                 # total_tokens = response['usage']['total_tokens']
#                 # text_tokens = response['usage']['prompt_tokens_details']['text_tokens']
#                 # audio_tokens = response['usage']['prompt_tokens_details']['audio_tokens']
#                 # image_tokens = response['usage']['prompt_tokens_details']['image_tokens']
#                 # cached_tokens = response['usage']['prompt_tokens_details']['cached_tokens']

#                 #print(content, total_tokens, text_tokens, audio_tokens, image_tokens, cached_tokens)

#                 # Tokens:
#                 if response:
#                     response_text = response['choices'][0]['message']['content']
#                     total_token_count = response['usage']['total_tokens']
#                 else:
#                     logging.error("No response from Grok.")
#                     return {"response": "No response from Grok."}

#                 model_version = model_name
#                 used_tokens = total_token_count

#                 # Calculation of money spent on tokens
#                 expenses = await calculate_token_cost(access_id, model_version, used_tokens, input_data="text")

#                 return {"response": response_text, "expenses": expenses, "used_tokens": used_tokens}
            
#             except:
#                 return {"response": response, "expenses": 0, "used_tokens": 0}











            # content_type = response.headers.get('Content-Type', '').lower()
            
            # if 'application/json' in content_type:
            #     result = await response.json()
            # else:
            #     result = await response.text()
            #     print(result)
            #     print(type(result))
            #     return result