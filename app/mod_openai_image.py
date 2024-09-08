from openai import AsyncOpenAI, RateLimitError, OpenAIError
from openai import OpenAI
from keys import api_key_openai
from general_functions import cleaner_model

from PIL import Image
import io
import base64



    # 'dall-e-3-1024': 0.08,
    # 'dall-e-3-1792': 0.16,

    # 'dall-e-3-hd-1024': 0.16,
    # 'dall-e-3-hd-1792': 0.24,

    # 'dall-e-2-1024': 0.04,
    # 'dall-e-2-512': 0.036,
    # 'dall-e-2-256': 0.032,




client = AsyncOpenAI(api_key=api_key_openai)

async def mod_dall_e(description, image_path):

    username = description.get("username")
    user_content = description.get("user_content")
    size = description.get("size", "1024x1024")
    quality = description.get("quality", "standart")
    response_format = description.get("response_format", "url")
    n = description.get("n", 1)
    style = description.get("style", "Natural")
    model = description.get("model", "dall-e-3")
    real_name_model = await cleaner_model(model)

    params = {
    'prompt': user_content,
    'model': real_name_model,
    'size': size,
    'response_format': response_format,  # url or b64_json
    }

    if not image_path:
        if real_name_model == "dall-e-3":
            params['quality'] = quality
            params['style'] = style


        if real_name_model == "dall-e-2":
            params['n'] = n


        response = await client.images.generate(**params)

    if image_path:
        if real_name_model == "dall-e-3":
            params['quality'] = quality


        if real_name_model == "dall-e-2":
            params['n'] = n

        # Открываем изображение
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()

        # Кодируем изображение в base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        params['image'] = image_base64

        # Формируем запрос к API DALL-E для редактирования изображения
        response = await client.images.edit(**params)




    #return response['data'][0]['url']  # Возвращаем URL измененного изображения
    print(response.data[0].url)
    return response.data[0].url




'''

prompt - Текстовое описание желаемого изображения (изображений). Максимальная длина - 1000 символов для dall-e-2 и 4000 символов для dall-e-3

quality - Качество генерируемого изображения. hd создает изображения с более мелкими деталями и большей согласованностью по всему изображению. 
Этот параметр поддерживается только для dall-e-3. По умолчанию установлено стандартное значение.

Количество генерируемых изображений. Должно быть от 1 до 10. Для dall-e-3 поддерживается только n=1.

size - Размер генерируемых изображений. Должен быть одним из 256x256, 512x512 или 1024x1024 для моделей dall-e-2. Должно быть одно из 
1024x1024, 1792x1024 или 1024x1792 для моделей dall-e-3.

response_format - Формат, в котором будут возвращены сгенерированные изображения. Должен быть одним из url или b64_json. URL действительны только в течение 60 минут 
после создания изображения.

style - Стиль создаваемых изображений. Должен быть одним из ярких или естественных. Vivid заставляет модель склоняться к созданию гиперреальных 
и драматических изображений. Natural заставляет модель создавать более естественные, менее гиперреалистичные изображения. Этот параметр поддерживается 
только для dall-e-3.

'''




    # if image_path:

    #     # Открываем изображение
    #     with open(image_path, 'rb') as img_file:
    #         image_data = img_file.read()

    #     # Кодируем изображение в base64
    #     image_base64 = base64.b64encode(image_data).decode('utf-8')

    #     # Формируем запрос к API DALL-E для редактирования изображения
    #     response = await client.images.edit(**params)
    #     # response = await client.images.edit(
    #     #     prompt = user_content,
    #     #     image = image_base64,
    #     #     model = real_name_model,
    #     #     size = size,
    #     #     quality = quality, # hd or standard
    #     #     response_format = response_format, # url or b64_json
    #     #     style = style, # Vivid or Natural only dall-e-3
    #     #     n = n, # Колличество картинок
    #     # )

