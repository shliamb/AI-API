from openai import AsyncOpenAI, RateLimitError, OpenAIError
from openai import OpenAI
from keys import api_key_openai



#client = OpenAI(api_key=api_key_openai)
client = AsyncOpenAI(api_key=api_key_openai)

prompt = "Продавщица в магазине старая"
model = "dall-e-3"


async def mod_dall_e(username, description):
    # Generate an image based on the prompt
    response = await client.images.generate(
        prompt=prompt,
        model=model,
        size="1024x1024",  # 1024x1024
        n=1, # Колличество картинок
    )

    # Prints response containing a URL link to image
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