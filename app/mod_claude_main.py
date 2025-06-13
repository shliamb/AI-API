from config import LOG_CONFIG_AI, DEF_CLAUDE_VERSION, TIMEOUT_SERVER_AI
import logging
logging.basicConfig(**LOG_CONFIG_AI)
import asyncio
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

    logging.info(f"{access_id} -> 'main API CLAUDE ANTHROPIC'")
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



    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers, timeout=TIMEOUT_SERVER_AI) as response:
                try:
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
                    expenses = await calculate_token_cost(access_id, model_version, used_tokens, input_data="text")
                    return {"response": response_text, "expenses": expenses, "used_tokens": used_tokens}
                
                except:
                    return {"response": response, "expenses": 0, "used_tokens": 0}

    except asyncio.TimeoutError:
        logging.error("TimeoutError of CLAUDE ANTHROPIC Server")
        return {"response": "TimeoutError of CLAUDE ANTHROPIC Server", "expenses": 0, "used_tokens": 0}
    
    except Exception as e:
        logging.error(f"UnexpectedError of CLAUDE ANTHROPIC main: {str(e)}")
        return {"response": f"UnexpectedError of CLAUDE ANTHROPIC main: {str(e)}", "expenses": 0, "used_tokens": 0}
