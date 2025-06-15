from config import LOG_CONFIG_API, DEF_CLAUDE_VERSION, TIMEOUT_SERVER_AI, setup_logger
logger_api = setup_logger('api', LOG_CONFIG_API)
#import asyncio
import aiohttp
from keys import API_KEY_CLAUDE
from general_functions import DictObj, encode_file
from store_token_cost import calculate_token_cost





# Main Text ANTHROPIC Function
async def claude_text(description: dict) -> dict:
    '''Основной модуль CLAUDE ANTHROPIC'''

    dict_des = DictObj(description)
    access_id = dict_des.access_id
    user_content = dict_des.user_content
    system_content = dict_des.system_content
    model_name = dict_des.model
    file_path = dict_des.file_path
    assist_content = dict_des.assist_content
    # tools = description.get("tools")
    # ?? 'response_format':'[generationConfig: {responseMimeType: "application/json",responseSchema: {type: SchemaType.ARRAY,items: {type: SchemaType.OBJECT,properties: {recipe_name: {type: SchemaType.STRING,},},},},}});]'

    logger_api.info(f"{access_id} -> 'main API CLAUDE ANTHROPIC'")
    print(f"INFO: {access_id} -> 'main API CLAUDE ANTHROPIC'")


    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": API_KEY_CLAUDE,
        "anthropic-version": DEF_CLAUDE_VERSION,
        "content-type": "application/json"
    }

    data = {}
    contents = []

    if file_path:
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

    max_tokens = 4096
    if model_name == "claude-3-5-sonnet-latest" or model_name == "claude-3-5-haiku-latest":
        max_tokens = 8192

    data["max_tokens"] = max_tokens
    data["messages"] = contents
    data["model"] = model_name

    if system_content:
        data["system"] = system_content



    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers, timeout=TIMEOUT_SERVER_AI) as response:

            try:
                result = await response.json()
            except:
                text_data = await response.text()
                return {"response": text_data, "expenses": 0, "used_tokens": 0}

            # Tokens:
            try:
                response_text = result['content'][0]['text']
                used_tokens = result['usage']['input_tokens'] + result['usage']['output_tokens']
            except:
                return {"response": result, "expenses": 0, "used_tokens": 0}

            # Calculation of money spent on tokens
            expenses = await calculate_token_cost(access_id, model_name, used_tokens, input_data="text")
            return {"response": response_text, "expenses": expenses, "used_tokens": used_tokens}
        
