# Base
from keys import API_KEY_CLAUDE
import logging
import aiohttp
import asyncio
# Claude
# import anthropic
# Service
from general_functions import calculation, encode_file
from config import default_model_claude, default_antropic_version





# Main Text ANTHROPIC Function
async def mod_claude(description, image_path):

    username = description.get("username")
    user_content = description.get("user_content")
    system_content = description.get("system_content")
    model_name = description.get("model", default_model_claude)
    # tools = description.get("tools")
    assist_content = description.get("assist_content")
    # ?? 'response_format':'[generationConfig: {responseMimeType: "application/json",responseSchema: {type: SchemaType.ARRAY,items: {type: SchemaType.OBJECT,properties: {recipe_name: {type: SchemaType.STRING,},},},},}});]'



    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": API_KEY_CLAUDE,
        "anthropic-version": default_antropic_version,
        "content-type": "application/json"
    }

    data = {}
    contents = []

    if image_path:
        encoded_image = await encode_file(image_path)
        contents.append({"role": "user", "content": [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": encoded_image,}}]})
        contents.append({"type": "text", "text": user_content})


    else:
        if assist_content:
            for one in assist_content:
                if "user" in one:
                    contents.append({"role": "user", "content": one["user"]},)
                if "assistant" in one:
                    contents.append({"role": "assistant", "content":one["assistant"]},)
        if user_content:
            contents.append({"role": "user", "content": user_content},)

    data["messages"] = contents
    data["model"] = model_name

    # if system_content:
    #     data["system"] = system_content



    print(data)



    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            response = await response.json()
            print(response)



            # # Tokens:
            # if response:
            #     response_text = response['candidates'][0]['content']['parts'][0]['text']
            #     total_token_count = response['usageMetadata']['totalTokenCount'] # totalTokenCount - это все токены и на входе и на выходе.
            # else:
            #     logging.error("No response from Google Gemini.")
            #     return {"response": "No response from Google Gemini."}

            # model_version = model_name
            # used_tokens = total_token_count

            # # Calculation of money spent on tokens
            # expenses = await calculation(username, model_version, used_tokens, input_data="text")

            # return {"response": response_text, "expenses": expenses, "used_tokens": used_tokens}















# client = anthropic.Anthropic(api_key=API_KEY_CLAUDE)

# message = client.messages.create(
#     model="claude-3-5-sonnet-20241022",
#     max_tokens=1024,
#     system="Вы первоклассный поэт. Отвечайте только короткими стихами.",
#     messages=[
#         {"role": "user", "content": "Hello, Claude"}
#     ]
# )



    #     [
    # {"role": "user", "content": "Hello there."},
    # {"role": "assistant", "content": "Hi, I'm Claude. How can I help you?"},
    # {"role": "user", "content": "Can you explain LLMs in plain English?"},
    # ]


    # {"role": "user", "content": "Hello, Claude"}
    
    # {"role": "user", "content": [{"type": "text", "text": "Hello, Claude"}]}



    # {"role": "user", "content": [
    # {
    #     "type": "image",
    #     "source": {
    #     "type": "base64",
    #     "media_type": "image/jpeg", # image/jpeg, image/png, image/gif, and image/webp
    #     "data": "/9j/4AAQSkZJRg...",
    #     }
    # },
    # {"type": "text", "text": "What is in this image?"}
    # ]}


# message_list = [
#     {
#         "role": 'user',
#         "content": [
#             {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": get_base64_encoded_image("../images/best_practices/nine_dogs.jpg")}},
#             {"type": "text", "text": "How many dogs are in this picture?"}
#         ]
#     }
# ]





# print(message.content)















# import base64
# import httpx

# image1_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
# image1_media_type = "image/jpeg"
# image1_data = base64.standard_b64encode(httpx.get(image1_url).content).decode("utf-8")

# image2_url = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg"
# image2_media_type = "image/jpeg"
# image2_data = base64.standard_b64encode(httpx.get(image2_url).content).decode("utf-8")



# import anthropic

# client = anthropic.Anthropic()
# message = client.messages.create(
#     model="claude-3-5-sonnet-20241022",
#     max_tokens=1024,
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "image",
#                     "source": {
#                         "type": "base64",
#                         "media_type": image1_media_type,
#                         "data": image1_data,
#                     },
#                 },
#                 {
#                     "type": "text",
#                     "text": "Опишите это изображение."
#                 }
#             ],
#         }
#     ],
# )
# print(message)