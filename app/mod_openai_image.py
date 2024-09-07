from openai import OpenAI
from keys import api_key_openai



client = OpenAI(api_key=api_key_openai)
#client = AsyncOpenAI(api_key=api_key_openai)

prompt = "A cute baby sea otter"
model = "dall-e-3"


async def mod_dall_e(username, description):
    # Generate an image based on the prompt
    response = client.images.generate(
        prompt=prompt,
        model=model,
        size="1024x1024",
        n=2,
    )

    # Prints response containing a URL link to image
    print(response.data[0].url)
    return response.data[0].url







# from openai import OpenAI
# client = OpenAI()

# response = client.images.generate(
#     prompt="A cute baby sea otter",
#     n=2,
#     size="1024x1024"
# )

# print(response.data[0].url)