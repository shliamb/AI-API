from config import TIMEOUT_SERVER_AI
from setup_config_logger import setup_logger
logger_ai = setup_logger('ai', '/log/ai.log')
from keys import API_KEY_OPENAI
import asyncio
from openai import AsyncOpenAI, OpenAIError
from general_functions import DictObj, cleaner_model
from store_token_cost import calculate_token_cost



client = AsyncOpenAI(api_key=API_KEY_OPENAI)


#### Create image
async def openai_img(description):
    '''Генерация картинок от OpenAI'''

    dict_des = DictObj(description)
    access_id = dict_des.access_id
    user_content = dict_des.user_content
    size = dict_des.size
    quality = dict_des.quality
    response_format = dict_des.response_format
    n = dict_des.n
    style = dict_des.style
    model = dict_des.model
    real_name_model = await cleaner_model(model) # dall-e-3

    logger_ai.info(f"{access_id} -> 'img-gen API OpenAI'")
    print(f"INFO: {access_id} -> 'img-gen API OpenAI'")

    params = {
        "prompt": user_content,
        "size": size,
        "response_format": response_format,  # url or b64_json
        "model": real_name_model
    }

    if real_name_model == "dall-e-3":
        params['quality'] = quality
        params['style'] = style

    elif real_name_model == "dall-e-2":
        params['n'] = n

    try:
        response = await asyncio.wait_for(client.images.generate(**params), timeout=TIMEOUT_SERVER_AI)
        #print(f"INFO: 'main API OpenAI' -> get response")
        logger_ai.info(f"'main API OpenAI' -> get response")

    except asyncio.TimeoutError:
        logger_ai.error("TimeoutError of OpenAI gen-img Server")
        return {"response": "TimeoutError of OpenAI gen-img Server", "expenses": 0, "pictures": n}
    
    except OpenAIError as e:
        logger_ai.error(f"OpenAIError gen-img: {str(e)}")
        return {"response": f"OpenAIError gen-img: {str(e)}", "expenses": 0, "pictures": n}
    
    except Exception as e:
        logger_ai.error(f"UnexpectedError OpenAI gen-img: {str(e)}")
        return {"response": f"UnexpectedError OpenAI gen-img: {str(e)}", "expenses": 0, "pictures": n}


    # TOKENS:
    try:
        used_tokens = n
        model_version = model # exemple - dall-e-3-hd-1792
        response_img = response.data[0].url

        # Calculation of money spent on tokens
        expenses = await calculate_token_cost(access_id, model_version, used_tokens, input_data="img")
        return {"response": response_img, "expenses": expenses, "pictures": n}

    except:
        response_content = response.output_text
        logger_ai.error(f"Error: Failed to calculate tokens OpenAI: {e}")
        return {"response": response_content, "expenses": 0, "used_tokens": 0}























'''

Условия использования API OpenAI:

client.images.generate - Генерация нового изображения

! prompt (str) - Текстовое описание желаемого изображения (изображений). Максимальная длина - 1000 символов для dall-e-2 и 4000 символов для dall-e-3

quality (str) - Качество генерируемого изображения. hd создает изображения с более мелкими деталями и большей согласованностью по всему изображению. 
Этот параметр поддерживается только для dall-e-3. По умолчанию установлено стандартное значение. standard

n (int) - Количество генерируемых изображений. Должно быть от 1 до 10. Для dall-e-3 поддерживается только n=1.

size (str)  - Размер генерируемых изображений. Должен быть одним из 256x256, 512x512 или 1024x1024 для моделей dall-e-2. Должно быть одно из 
1024x1024, 1792x1024 или 1024x1792 для моделей dall-e-3.

response_format (str) - Формат, в котором будут возвращены сгенерированные изображения. Должен быть одним из url или b64_json. URL действительны только в течение 60 минут 
после создания изображения.

style (str) - Стиль создаваемых изображений. Должен быть одним из ярких или естественных. vivid заставляет модель склоняться к созданию гиперреальных 
и драматических изображений. Natural заставляет модель создавать более естественные, менее гиперреалистичные изображения. Этот параметр поддерживается 
только для dall-e-3.

'''

