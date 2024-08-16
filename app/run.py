import asyncio
from openai import AsyncOpenAI, RateLimitError, OpenAIError
from fastapi import FastAPI, Header, Depends, HTTPException, status
from pydantic import BaseModel
from keys import api_key_openai, my_key

client = AsyncOpenAI(api_key=api_key_openai)
app = FastAPI()



# Checking the api_key user
# def verify_api_key(api_key: str = Header(...)):
#     if api_key != my_key:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Invalid API Key",
#         )

# Model Text Chat GPT
class UserInput(BaseModel):
    prompt: str

# Endpoint Text Chat GPT
@app.post("/chat/", status_code=status.HTTP_201_CREATED)
async def chat(user_input: UserInput, api_key: str = Header(...)): # api_key: str = Depends(verify_api_key)):


    if str(api_key) != str(my_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )

    '''
    API Sample Question:
        {
            "prompt": "Как ты бро?",
            "model": "gpt-4o-mini-2024-07-18",

        }
    '''

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
        raise HTTPException(status_code=500, detail=f"Ошибка какая то {str(e)}")






if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000) # При деплое переделать