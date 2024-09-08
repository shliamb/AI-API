from openai import AsyncOpenAI, RateLimitError, OpenAIError
import logging
# from openai import OpenAI
from keys import api_key_openai
from general_functions import cleaner_model
from general_functions import calculation


from PIL import Image
import io
import base64



client = AsyncOpenAI(api_key=api_key_openai)



# Function to encode the image
async def encode_image(image_path):
  with open(image_path, "rb") as image_path:
    return base64.b64encode(image_path.read()).decode('utf-8')


async def mod_dall_e(description, image_path):

    username = description.get("username")
    user_content = description.get("user_content")
    size = description.get("size", "1024x1024")
    quality = description.get("quality", "standard") # hd ore standard
    response_format = description.get("response_format", "url") # b64_json
    n = description.get("n", 1)
    style = description.get("style", "natural") # vivid ore natural
    model = description.get("model", "dall-e-2-1024")
    real_name_model = await cleaner_model(model) # dall-e-3

    params = {
    'prompt': user_content,
    'size': size,
    'response_format': response_format,  # url or b64_json
    }


    if not image_path:
        print("!!!!!!!!!!!! 1")
        if real_name_model == "dall-e-3":
            params['model'] = real_name_model
            params['quality'] = quality
            params['style'] = style


        if real_name_model == "dall-e-2":
            params['model'] = real_name_model
            params['n'] = n

        response = await client.images.generate(**params)


    if image_path:
        print("!!!!!!!!!!!! 2")
        params['model'] = "dall-e-2"
        params['n'] = n

        base64_file = await encode_image(image_path)
        params['image'] = base64_file # open(image_path, "rb"),


        print(params)




        # Формируем запрос к API DALL-E для редактирования изображения
        response = await client.images.edit(**params)

        # client.images.edit(
        #                     image=open("otter.png", "rb"),
        #                     mask=open("mask.png", "rb"),
        #                     prompt="A cute baby sea otter wearing a beret",
        #                     n=2,
        #                     size="1024x1024"
        #                     )




    # Statistic
    used_tokens = n * 1000000 # У меня цены в price за 1мл токенов, а картинки то по одной
    model_version = model # exemple - dall-e-3-hd-1792
    
    # Calculation of money spent on tokens
    expenses = await calculation(username, model_version, used_tokens)

    return {"response": response.data[0].url, "expenses": expenses, "pictures": n}




'''

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







'''

client.images.edit - Создает отредактированное или расширенное изображение на основе исходного изображения и подсказки.


! image (file) - Изображение для редактирования. Должно быть действительным PNG-файлом, размером менее 4 МБ и квадратным. Если маска не указана, изображение 
должно иметь прозрачность, которая будет использоваться в качестве маски.


! prompt (str) - Текстовое описание желаемого изображения (изображений). Максимальная длина - 1000 символов.


mask (file) - Дополнительное изображение, полностью прозрачные области которого (например, где альфа равна нулю) указывают на места, где изображение должно 
быть отредактировано. Должен быть действительным PNG-файлом, размером менее 4 МБ и иметь те же размеры, что и изображение.

model (str) - Модель, используемая для генерации изображений. На данный момент поддерживается только dall-e-2.


n (int) - Количество генерируемых изображений. Должно быть от 1 до 10.


size (str) - Размер генерируемых изображений. Должен быть одним из 256x256, 512x512 или 1024x1024.


response_format (str) - Формат, в котором будут возвращены сгенерированные изображения. Должен быть одним из url или b64_json. 
URL действительны только в течение 60 минут после создания изображения.





'''