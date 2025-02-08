# Base
from keys import API_KEY_GROK
import logging
import aiohttp
import asyncio
# Service
from general_functions import calculation, encode_file
from config import default_model_grok



# Main Text GROK Function
async def mod_grok(description, image_path):

    username = description.get("username")
    user_content = description.get("user_content")
    system_content = description.get("system_content")
    model_name = description.get("model", default_model_grok)
    # tools = description.get("tools")
    assist_content = description.get("assist_content")
    # ?? 'response_format':'[generationConfig: {responseMimeType: "application/json",responseSchema: {type: SchemaType.ARRAY,items: {type: SchemaType.OBJECT,properties: {recipe_name: {type: SchemaType.STRING,},},},},}});]'



    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY_GROK}"
    }

    data = {}
    contents = []

    if image_path: # ? 
        encoded_image = await encode_file(image_path)
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
        async with session.post(url, json=data, headers=headers) as response:
            response = await response.json()
            print(response)

            # input_tokens = response['usage']['input_tokens']
            # output_tokens = response['usage']['output_tokens']

            # # Tokens:
            # if response:
            #     response_text = response['content'][0]['text']
            #     total_token_count = input_tokens + output_tokens
            # else:
            #     logging.error("No response from Grok.")
            #     return {"response": "No response from Grok."}

            # model_version = model_name
            # used_tokens = total_token_count

            # # Calculation of money spent on tokens
            # expenses = await calculation(username, model_version, used_tokens, input_data="text")

            #return {"response": response_text, "expenses": expenses, "used_tokens": used_tokens}
            return {"response": response, "expenses": 0, "used_tokens": 0}

















    # data = {
    #     "messages": [
    #         {"role": "system", "content": "You are a test assistant."},
    #         {"role": "user", "content": "Testing. Just say hi and hello world and nothing else."}
    #     ],
    #     "model": "grok-2-latest",
    #     "stream": False,
    #     "temperature": 0
    # }