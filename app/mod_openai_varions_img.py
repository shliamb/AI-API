from openai import AsyncOpenAI, RateLimitError, OpenAIError
import logging
from keys import api_key_openai
from general_functions import cleaner_model
from general_functions import calculation


client = AsyncOpenAI(api_key=api_key_openai)


# Dall-e 2 variations img:
async def variations_dall_e(description, image_path):

    username = description.get("username")
    size = description.get("size", "1024x1024")
    response_format = description.get("response_format", "url") # b64_json
    n = description.get("n", 1)
    model = description.get("model", "dall-e-2-1024")
    real_name_model = await cleaner_model(model) # dall-e-2


    with open(image_path, "rb") as image_res:

        response = await client.images.create_variation(
                image = open(image_res, "rb"),
                model = real_name_model,
                response_format = response_format,
                n = n,
                size = size
        )

    # Statistic
    used_tokens = n
    model_version = model # exemple - dall-e-3-hd-1792
    
    # Calculation of money spent on tokens
    expenses = await calculation(username, model_version, used_tokens, input_data="img")

    return {"response": response.data[0].url, "expenses": expenses, "pictures": n}





'''
Условия API на стороне OpenAI:


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