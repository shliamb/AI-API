import logging
# Base
import asyncio
from pydantic import BaseModel
# Fasapi
from fastapi import FastAPI, Header, Depends, HTTPException, status
import uvicorn
import gunicorn
# Service
from worker_db import get_user_by_username, update_user
from general_functions import day_utcnow, unformat_date
from mod_openai import mod_openai
from config import limit_trying, timeout_after_error_username, waiting_time, time_correction


app = FastAPI()



#### OPENAI TEXT ####

'''
Post API Key to Heads
    {
        "username": "vlad", 
        "user_content": "поясни за физику?",
        "system_content": "ты преподаватель физики",
        "model": "gpt-4o-mini-2024-07-18",

    }
'''


# USER VERIFICATION
async def verify_user_appkey(username: str, appkey: str):
    data_by_username = await get_user_by_username(username)
    
    if data_by_username is None:
        await asyncio.sleep(timeout_after_error_username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid UserName in Body! After a failed attempt, a 5-second wait is activated. To register - https://t.me/myapi_aibot",
        )

    if data_by_username.is_block is True:

        un_waiting_time = float(0.01 * float(waiting_time))

        date_now = await day_utcnow(time_correction)
        un_date_now = await unformat_date(date_now)
        un_date_block = await unformat_date(data_by_username.date_block)
        un_time = un_date_now[1] - un_date_block[1]

        if un_date_now[0] == un_date_block[0] and un_time < un_waiting_time:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Sorry, the user is blocked for {waiting_time} minutes, after {limit_trying} unsuccessful attempts.",
            )
        
        if un_date_now[0] != un_date_block[0] or un_time >= un_waiting_time:
            updated_data = {"is_block": False, "is_failed": 0}
            await update_user(data_by_username.id, updated_data)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Congratulations! The time for blocking the user has passed, try again to access the API with the correct data.",
            )

    if appkey != str(data_by_username.appkey) and data_by_username.is_failed < limit_trying:
        new_limit = data_by_username.is_failed + 1
        updated_data = {"is_failed": new_limit}
        await update_user(data_by_username.id, updated_data)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid API Key, {new_limit} attempt out of {limit_trying}.",
        )
    
    if appkey != str(data_by_username.appkey) and data_by_username.is_failed >= limit_trying:
        updated_data = {"is_block": True, "date_block":  await day_utcnow(time_correction) } 
        await update_user(data_by_username.id, updated_data)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid API Key, valid attempts have ended, sorry, try again in {waiting_time} minutes.",
        )

    if data_by_username.money <= 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient funds. Please add funds to your account.",
        )

    if appkey == str(data_by_username.appkey) and data_by_username.is_failed != 0:
        updated_data = {"is_failed": 0}
        await update_user(data_by_username.id, updated_data)
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "The user has successfully logged in, the counters have been reset!"
        }
    
    if appkey == str(data_by_username.appkey):
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "The user has passed."
        }




# Model OPENAI TEXT
class UserInput(BaseModel):
    user_content: str
    system_content: str
    username: str
    model: str


# MAIN Endpoint
@app.get("/api/", status_code=status.HTTP_200_OK)
async def hello_api(): 
    return {"response": "https://t.me/myapi_aibot"}


# TEXT OPENAI Endpoint
@app.post("/api/chat/", status_code=status.HTTP_200_OK)
async def chat(user_input: UserInput, appkey: str = Header(...)):

    # Verify user and her appkey
    username = user_input.username
    confirm_verify = await verify_user_appkey(username, appkey)
    if confirm_verify["status_code"] != status.HTTP_200_OK:
        raise

    # Working with OpenAI
    confirm_openai = await mod_openai(username, user_input)

    if confirm_openai == "Error: There is no money for OpenAI account.":
        logging.info("There is no money for OpenAI account.")
        # Передача сигнала телеграмм боту, администратору

    return confirm_openai






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) # При деплое переделать