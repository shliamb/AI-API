from openai import AsyncOpenAI, RateLimitError, OpenAIError
from openai import OpenAI
from keys import api_key_openai



#client = OpenAI(api_key=api_key_openai)
client = AsyncOpenAI(api_key=api_key_openai)

prompt = "Продавщица в магазине старая"
model = "dall-e-3"


async def mod_dall_e(username, description):

    response = await client.images.generate(
        prompt=prompt,
        model=model,
        size="1024x1024", 
        n=1, # Колличество картинок
    )


    print(response.data[0].url)
    return response.data[0].url




# - '256x256'
# - '512x512'
# - '1024x1024'
# - '1024x1792'
# - '1792x1024'


# from openai import OpenAI
# client = OpenAI()

# response = client.images.generate(
#     prompt="A cute baby sea otter",
#     n=2,
#     size="1024x1024"
# )

# print(response.data[0].url)








# from PIL import Image
# import io
# import base64

# async def mod_dall_e(username, image_path, description):
#     # Открываем изображение
#     with open(image_path, 'rb') as img_file:
#         image_data = img_file.read()
    
#     # Кодируем изображение в base64
#     image_base64 = base64.b64encode(image_data).decode('utf-8')

#     # Формируем запрос к API DALL-E для редактирования изображения
#     response = await client.images.edit(
#         prompt=description,
#         image=image_base64,
#         model='dall-e',  # Убедитесь, что используете правильную модель
#         size="1024x1024", 
#         n=1  # Количество картинок
#     )

#     return response['data'][0]['url']  # Возвращаем URL измененного изображения

# # Пример использования функции
# username = "example_user"
# image_path = "path/to/your/image.jpg"
# description = "Изменить фон на звездное небо"

# # Вызов функции (в контексте асинхронного выполнения)
# modified_image_url = await mod_dall_e(username, image_path, description)
# print(modified_image_url)
