import asyncio
from openai import AsyncOpenAI, RateLimitError, OpenAIError
from fastapi import FastAPI, Header, Depends, HTTPException, status
from pydantic import BaseModel
from instruction import readme
from keys import api_key_openai

client = AsyncOpenAI(api_key=api_key_openai)
app = FastAPI()



# One Sample Question to API:
'''
Post API Key to Heads
    {
        "username": "vlad",
        "prompt": "Как ты бро?",
        "model": "gpt-4o-mini-2024-07-18",

    }
'''


# Endpoint Just Instruction To Work API
@app.get("/api/", status_code=status.HTTP_200_OK)
async def hello_api(): 
    return {"response": readme}


# Checking the api_key user
# Переделать позже, под работу с базой данных...
def verify_user_appkey(username: str, appkey: str):

    if username != "vlad":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Name User",
        )

    if appkey != "fdft5jhy5445dfftghd334":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )




# Model Text Chat GPT
class UserInput(BaseModel):
    prompt: str
    username: str
    model: str




# Endpoint Text Chat GPT
@app.post("/api/chat/", status_code=status.HTTP_200_OK)
async def chat(user_input: UserInput, appkey: str = Header(...)):

    # Verify user and her appkey
    username = user_input.username
    verify_user_appkey(username, appkey)


    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Ты сексуальная девушка, которая общается очень сексуально и с заигрыванием."}, # Определение роли AI
                {"role": "user", "content": user_input.prompt}, # Сообщение от пользователя для AI
                ],
                model=user_input.model,
        )
        
        # Извлечение ответа из результата
        response_content = chat_completion.choices[0].message.content
        
        return {"response": response_content}
    
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка какая то {str(e)}")





# from openai import OpenAI
# client = OpenAI()

# response = client.images.generate(
#     prompt="A cute baby sea otter",
#     n=2, # Список из двух изображений
#     size="1024x1024"
# )

# print(response.data[0].url)





if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000) # При деплое переделать