from openai import OpenAI
from keys import api_key_openai


client = OpenAI(api_key=api_key_openai)

response = client.embeddings.create(
    model="text-embedding-3-large",
    input="The food was delicious and the waiter..."
)

print(response)