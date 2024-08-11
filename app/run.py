import asyncio
from openai import AsyncOpenAI, RateLimitError, OpenAIError
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from keys import api_key_openai

client = AsyncOpenAI(api_key=api_key_openai)

app = FastAPI()


# Модель запроса для получения текста от пользователя
class UserInput(BaseModel):
    prompt: str

@app.post("/chat/")
async def chat(user_input: UserInput):
    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input.prompt,
                }
            ],
            model="gpt-4o-mini",
        )
        
        # Извлечение ответа из результата
        response_content = chat_completion.choices[0].message['content']
        
        return {"response": response_content}
    
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)