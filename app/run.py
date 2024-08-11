import asyncio
from openai import AsyncOpenAI, RateLimitError, OpenAIError
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from keys import api_key_openai, my_key

client = AsyncOpenAI(api_key=api_key_openai)

app = FastAPI()


# Модель запроса для получения текста от пользователя
class UserInput(BaseModel):
    prompt: str

@app.post("/chat/")
async def chat(user_input: UserInput, x_api_key: str = Header(...)):

    # Проверка api_key
    print(my_key)
    if x_api_key != my_key:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input.prompt,
                }
            ],
            model="gpt-4o-mini-2024-07-18",
        )
        
        # Извлечение ответа из результата
        response_content = chat_completion.choices[0].message.content
        
        return {"response": response_content}
    
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)