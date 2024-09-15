from openai import AsyncOpenAI, RateLimitError, OpenAIError
import logging
from keys import api_key_openai
from general_functions import cleaner_model
from general_functions import calculation




client = AsyncOpenAI(api_key=api_key_openai)




async def mod_edit_dall_e(description, image_path, mask_path):

    username = description.get("username")
    user_content = description.get("user_content")
    size = description.get("size", "1024x1024")
    # quality = description.get("quality", "standard") # hd ore standard
    response_format = description.get("response_format", "url") # b64_json
    n = description.get("n", 1)
    # style = description.get("style", "natural") # vivid ore natural
    model = description.get("model", "dall-e-2-1024")
    real_name_model = await cleaner_model(model) # dall-e-2



    if mask_path:

        with open(image_path, 'rb') as image_file, \
            open(mask_path, 'rb') as mask_file:

            image = image_file.read()
            mask = mask_file.read()

            response = await client.images.edit(
                    image = image,
                    mask = mask,
                    prompt = user_content,
                    model = real_name_model,
                    response_format = response_format,
                    n = n,
                    size = size
            )

    elif not mask_path:

        with open(image_path, 'rb') as image_file:

            image = image_file.read()

            response = await client.images.edit(
                    image = image,
                    prompt = user_content,
                    model = real_name_model,
                    response_format = response_format,
                    n = n,
                    size = size
            )

    # Statistic
    used_tokens = n
    model_version = model # exemple - dall-e-2-1024
    # used_tokens = response.usage.total_tokens - их там тупо нету
    
    # Calculation of money spent on tokens
    expenses = await calculation(username, model_version, used_tokens, input_data="img")

    return {"response": response.data[0].url, "expenses": expenses, "pictures": n}




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