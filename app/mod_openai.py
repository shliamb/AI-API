# Base
import asyncio
# OpenAI
from openai import AsyncOpenAI, RateLimitError, OpenAIError
from keys import api_key_openai

client = AsyncOpenAI(api_key=api_key_openai)





async def mod_openai(user_input):


    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": user_input.system_content}, # Определение роли AI
                {"role": "user", "content": user_input.user_content}, # Сообщение от пользователя для AI
                ],
                model=user_input.model,
        )
        
        # Извлечение ответа из результата
        response_content = chat_completion.choices[0].message.content
        
        return {"response": response_content}


    except RateLimitError:
        return {"status_code":429, "detail": "Rate limit exceeded"}
    except OpenAIError as e:
        return {"status_code":500, "detail": f"Error: {str(e)}"}