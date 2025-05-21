# Base
from keys import API_KEY_CLAUDE
import logging
import aiohttp
import asyncio
# Claude
# import anthropic
# Service
from general_functions import calculation, encode_file
from config import DEF_MOD_CLAUDE, DEF_CLAUDE_VERSION



# Main Text ANTHROPIC Function
async def mod_claude(description, image_path):

    username = description.get("username")
    user_content = description.get("user_content")
    system_content = description.get("system_content")
    model_name = description.get("model", DEF_MOD_CLAUDE)
    # tools = description.get("tools")
    assist_content = description.get("assist_content")
    # ?? 'response_format':'[generationConfig: {responseMimeType: "application/json",responseSchema: {type: SchemaType.ARRAY,items: {type: SchemaType.OBJECT,properties: {recipe_name: {type: SchemaType.STRING,},},},},}});]'



    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": API_KEY_CLAUDE,
        "anthropic-version": DEF_CLAUDE_VERSION,
        "content-type": "application/json"
    }

    data = {}
    contents = []

    if image_path:
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

    max_tokens = 4096
    if model_name == "claude-3-5-sonnet-latest" or model_name == "claude-3-5-haiku-latest":
        max_tokens = 8192

    data["max_tokens"] = max_tokens
    data["messages"] = contents
    data["model"] = model_name

    if system_content:
        data["system"] = system_content


    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            response = await response.json()

            input_tokens = response['usage']['input_tokens']
            output_tokens = response['usage']['output_tokens']

            # Tokens:
            if response:
                response_text = response['content'][0]['text']
                total_token_count = input_tokens + output_tokens
            else:
                logging.error("No response from Anthropic Glaude.")
                return {"response": "No response from Anthropic Glaude."}

            model_version = model_name
            used_tokens = total_token_count

            # Calculation of money spent on tokens
            expenses = await calculation(username, model_version, used_tokens, input_data="text")

            return {"response": response_text, "expenses": expenses, "used_tokens": used_tokens}

