import asyncio
from openai import AsyncOpenAI, RateLimitError, OpenAIError
from fastapi import FastAPI, Header, Depends, HTTPException, status
from pydantic import BaseModel
from instruction import readme
from keys import api_key_openai, my_key

client = AsyncOpenAI(api_key=api_key_openai)
app = FastAPI()





# One Sample Question to API:
'''
    {
        "username": "vlad",
        "prompt": "Как ты бро?",
        "model": "gpt-4o-mini-2024-07-18",

    }
'''



# Endpoint Just Instruction To Work API
@app.get("/api/", status_code=status.HTTP_200_OK)
async def hello_api(): 
    return {readme}


# Checking the api_key user
def verify_user_appkey(username: str, appkey: str):

    if username != "vlad":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )

    if appkey != "fdft5jhy5445dfftghd334":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )

# Model Text Chat GPT
class UserInput(BaseModel):
    prompt: str


# Endpoint Text Chat GPT
@app.post("/api/chat/", status_code=status.HTTP_200_OK)
async def chat(user_input: UserInput, appkey: str = Header(...)):   # = Depends(verify_appkey)):

    # Verify user and her appkey
    verify_user_appkey(user_input.username, appkey)


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