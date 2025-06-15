from config import LOG_CONFIG_AI, TIMEOUT_SERVER_AI, setup_logger
logger_ai = setup_logger('ai', LOG_CONFIG_AI)
import asyncio
from openai import AsyncOpenAI, OpenAIError
from keys import API_KEY_OPENAI
from general_functions import DictObj, encode_file
from store_token_cost import calculate_token_cost



client = AsyncOpenAI(api_key=API_KEY_OPENAI)



logger_ai.info("INFO: Hi i am here, ai!")



# Основной модуль OpenAI:
async def openai_text(description: dict) -> dict:
    '''Основной модуль OpenAI'''

    dict_des = DictObj(description)
    access_id = dict_des.access_id
    user_content = dict_des.user_content
    system_content = dict_des.system_content
    model_name = dict_des.model
    assist_content = dict_des.assist_content
    response_format = dict_des.response_format
    file_path = dict_des.file_path

    logger_ai.info(f"{access_id} -> 'main API OpenAI'")
    print(f"INFO: {access_id} -> 'main API OpenAI'")


    # OpenAI:
    messages_ai = []

    if system_content: # if system_content and model_name not in ("o1-preview", "o1-mini", "o1", "o3-mini"):
        messages_ai.append({"role": "system", "content": system_content},)

    if file_path:
        base64_file = await encode_file(file_path)
        messages_ai.append({"role": "user", "content": [{"type": "input_text", "text": user_content}, {"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64_file}",},],},)
    else:
        if assist_content:
            for data in assist_content:
                if "user" in data:
                    messages_ai.append({"role": "user", "content": data["user"]})
                if "assistant" in data:
                    messages_ai.append({"role": "assistant", "content": data["assistant"]})
        if user_content:
            messages_ai.append({"role": "user", "content": user_content},)
        if not response_format:
            response_format = {"type": "text"}

    try:
        response = await asyncio.wait_for(client.responses.create(model = model_name, input = messages_ai), timeout=TIMEOUT_SERVER_AI)    #, #response_format = response_format, instructions = instructions
        #print(f"INFO: 'main API OpenAI' -> get response")
        logger_ai.info(f"'main API OpenAI' -> get response")

    except asyncio.TimeoutError:
        logger_ai.error("TimeoutError of OpenAI Server")
        return {"response": "TimeoutError of OpenAI Server", "expenses": 0, "used_tokens": 0}
    
    except OpenAIError as e:
        logger_ai.error(f"OpenAIError: {str(e)}")
        return {"response": f"OpenAIError: {str(e)}", "expenses": 0, "used_tokens": 0}
    
    except Exception as e:
        logger_ai.error(f"UnexpectedError of OpenAI main: {str(e)}")
        return {"response": f"UnexpectedError of OpenAI main: {str(e)}", "expenses": 0, "used_tokens": 0}



    # TOKENS:
    try:
        #response_id = response.id # !!!!
        #model_version = response.model
        response_content = response.output_text
        used_tokens = response.usage.total_tokens # + response.usage.prompt_tokens

        # Calculation of money spent on tokens
        expenses = await calculate_token_cost(access_id, model_name, used_tokens, input_data="text")
        return {"response": response_content, "expenses": expenses, "used_tokens": used_tokens}

    except:
        try:
            logger_ai.error(f"Error: Failed to calculate tokens OpenAI")
            return {"response": response_content, "expenses": 0, "used_tokens": 0}
        except:
            logger_ai.error(f"Error: Failed to calculate tokens OpenAI")
            return {"response": response, "expenses": 0, "used_tokens": 0}
































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



        #Response(id='resp_682bb086c8a48191afd03810ef04478d0896040cf9413041', created_at=1747693702.0, error=None, incomplete_details=None, instructions=None, metadata={}, model='chatgpt-4o-latest', object='response', output=[ResponseOutputMessage(id='msg_682bb0879d908191844aa9d74ca51e680896040cf9413041', content=[ResponseOutputText(annotations=[], text="Привет, Alex. I'm ready (готова) к работе — говори, что нужно.", type='output_text')], role='assistant', status='completed', type='message')], parallel_tool_calls=True, temperature=1.0, tool_choice='auto', tools=[], top_p=1.0, max_output_tokens=None, previous_response_id=None, reasoning=Reasoning(effort=None, generate_summary=None, summary=None), service_tier='default', status='completed', text=ResponseTextConfig(format=ResponseFormatText(type='text')), truncation='disabled', usage=ResponseUsage(input_tokens=113, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=21, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=134), user=None, store=True)



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