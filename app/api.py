import logging
logging.basicConfig(level=logging.INFO, filename='./log/api.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл
# Base
import asyncio
import aiofiles
# from pydantic import BaseModel
from typing import Optional
# import os
# import shutil
# import requests
# Fasapi
from fastapi import FastAPI, Header, Depends, HTTPException, status, UploadFile, File, Form
# from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import gunicorn
# Service
from worker_db import get_user_by_username, update_user
from general_functions import day_utcnow, unformat_date, remove_file_os, random_name_2X, encode_file
from mod_openai_main import mod_openai_text_img
from mod_gemini_main import mod_gemini
from mod_openai_gen_img import mod_gen_dall_e
from mod_openai_edit_img import mod_edit_dall_e
from mod_openai_varions_img import variations_dall_e
from mod_openai_text_to_audio import speech_to_audio_openai
from mod_openai_transcription import transcription_openai
from config import limit_trying, timeout_after_error_username, waiting_time, time_correction, price, uploads



app = FastAPI()


# Разрешаем CORS только для указанных эндпоинтов и метода POST
origins = ["*"]  # Разрешаем все источники (можно заменить на конкретные домены)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],  # Только метод POST
    allow_headers=["*"],
)



# USER VERIFICATION:
async def verify_user_appkey(username: str, model: str, appkey: str):
    data_by_username = await get_user_by_username(username)
    
    if data_by_username is None:
        await asyncio.sleep(timeout_after_error_username)
        logging.error("Invalid UserName in Body! After a failed attempt, a 5-second wait is activated.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid UserName in Body! After a failed attempt, a 5-second wait is activated. To register - https://t.me/myapi_aibot",
        )

    if data_by_username.is_block is True:

        un_waiting_time = float(0.01 * float(waiting_time))

        date_now = await day_utcnow()
        un_date_now = await unformat_date(date_now)
        un_date_block = await unformat_date(data_by_username.date_block)
        un_time = un_date_now[1] - un_date_block[1]

        if un_date_now[0] == un_date_block[0] and un_time < un_waiting_time:
            logging.error(f"Sorry, the user is blocked for {waiting_time} minutes, after {limit_trying} unsuccessful attempts.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Sorry, the user is blocked for {waiting_time} minutes, after {limit_trying} unsuccessful attempts.",
            )
        
        if un_date_now[0] != un_date_block[0] or un_time >= un_waiting_time:
            updated_data = {"is_block": False, "is_failed": 0}
            await update_user(data_by_username.id, updated_data)
            logging.error("Congratulations! The time for blocking the user has passed, try again to access the API with the correct data.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Congratulations! The time for blocking the user has passed, try again to access the API with the correct data.",
            )

    if appkey != str(data_by_username.appkey) and data_by_username.is_failed < limit_trying:
        new_limit = data_by_username.is_failed + 1
        updated_data = {"is_failed": new_limit}
        await update_user(data_by_username.id, updated_data)
        logging.error(f"Invalid API Key, {new_limit} attempt out of {limit_trying}.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid API Key, {new_limit} attempt out of {limit_trying}.",
        )
    
    if appkey != str(data_by_username.appkey) and data_by_username.is_failed >= limit_trying:
        updated_data = {"is_block": True, "date_block":  await day_utcnow() } 
        await update_user(data_by_username.id, updated_data)
        logging.error(f"Invalid API Key, valid attempts have ended, sorry, try again in {waiting_time} minutes.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid API Key, valid attempts have ended, sorry, try again in {waiting_time} minutes.",
        )

    if data_by_username.money <= 0:
        logging.error("Insufficient funds. Please add funds to your account.")
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient funds. Please add funds to your account.",
        )

    if model not in price:
        logging.error("Unfortunately, this model is not on the list.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unfortunately, this model is not on the list.",
        )

    if appkey == str(data_by_username.appkey) and data_by_username.is_failed != 0:
        updated_data = {"is_failed": 0}
        await update_user(data_by_username.id, updated_data)
        logging.info("The user has successfully logged in, the counters have been reset!")
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "The user has successfully logged in, the counters have been reset!"
        }
    
    if appkey == str(data_by_username.appkey):
        logging.info("The user has passed.")
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "The user has passed."
        }
####





#### OPEN AI ####

# TEXT & IMAGE OPENAI Endpoint:
@app.post("/api/openai_chat/", status_code=status.HTTP_200_OK)
async def openai_api(
    username: str = Form(...),                      # !
    # user_name   -->  {"role": "system", "name": "Alex", "content":
    # system_name
    user_content: str = Form(...),                  # !
    system_content: str = Form(None),               #
    model: str = Form(None),                        #
    appkey: str = Header(...),                      # !
    image: Optional[UploadFile] = File(None)        # # jpg, png проверенно
):

    # Choosing a price list.
    if not model:
        model = "gpt-4o-mini"

    # Verify user and her appkey
    confirm_verify = await verify_user_appkey(username, model, appkey)
    if confirm_verify["status_code"] != status.HTTP_200_OK:
        return confirm_verify

    if image:
        # Save img to server
        image_path = f"./uploads/{image.filename}"
        async with aiofiles.open(image_path, "wb") as buffer:
            while content := await image.read(1024):  # Читаем файл порциями по 1024 байта
                await buffer.write(content)
        # with open(image_path, "wb") as buffer:
        #     shutil.copyfileobj(image.file, buffer)
    else:
        image_path = None

    # Collect data
    description = {
        "username": username,
        "user_content": user_content,
        "model": model,
    }

    if system_content:
        description["system_content"] = system_content

    # Working with OpenAI
    confirm_openai = await mod_openai_text_img(description, image_path)

    # Remove file
    if image:
        remove = await remove_file_os(image_path)

    if confirm_openai == "Error: There is no money for OpenAI account.":
        logging.error("There is no money for OpenAI account.")
        # Передача сигнала телеграмм боту, администратору пока что хз как соеденить их)))

    return confirm_openai




#Create image DALL-E Endpoint:
@app.post("/api/gen-dall-e/", status_code=status.HTTP_200_OK)
async def dall_e_point(
    username: str = Form(...),              # !
    user_content: str = Form(...),          # !  dall-e-3 < 4000 and  dall-e-2 < 1000
    size: str = Form(None),                 # 1792 Only dall-e-3 and  512, 256 only dall-e-2
    quality: str = Form(None),              # Only dall-e-3 support hd, standard
    response_format: str = Form(None),      # url or b64_json
    n: int = Form(None),                    # dall-e-3 only 1 and dall-e-2 1 - 10
    style: str = Form(None),                # Only dall-e-3 support vivid ore natural
    model: str = Form(None),                # 
    appkey: str = Header(...),              # !
):
    
    # Check mistakes:
    if len(user_content) > 4000 and model == "dall-e-3":
        print("Error! Not support > 4000 simbol")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support > 4000 simbol",
        )

    if len(user_content) > 1000 and model == "dall-e-2":
        print("Error! Not support > 1000 simbols dall-e-2")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support > 1000 simbols dall-e-2",
        )

    if quality and model == "dall-e-2":
        print("Error! Not support quality dall-e-2.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support quality dall-e-2.",
        )

    if size and size == "1792x1024" and model == "dall-e-2":
        print("Error! Not support 1792x1024 to dall-e-2.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support 1792x1024 to dall-e-2.",
        )

    if size and size == "1024x1792" and model == "dall-e-2":
        print("Error! Not support 1024x1792 to dall-e-2.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support 1024x1792 to dall-e-2.",
        )

    if model == "dall-e-3":
        if size and size == "256x256" or size and size == "512x512":
            print("Error! Not support 512x512 and 256x256 to dall-e-3.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error! Not support 512x512 and 256x256 to dall-e-3.",
            )
        if n and n > 1:
            print("Error! Not support n > 1 to dall-e-3.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error! Not support n > 1 to dall-e-3.",
            )
        
    if model == "dall-e-2":
        if n and n > 10:
            print("Error! Not support n > 10 to dall-e-2.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error! Not support n > 10 to dall-e-2.",
            )
        if style:
            print("Error! Not support style to dall-e-2.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error! Not support style to dall-e-2.",
            )
        
    # Choosing a price list
    if model and model == "dall-e-3":
        if quality and quality == "hd":
            if size and size == "1024x1024":
                model = "dall-e-3-hd-1024"
            elif size and size == "1792x1024" or size and size == "1024x1792":
                model = "dall-e-3-hd-1792"
            else:
                model = "dall-e-3-hd-1024"
        elif quality and quality == "standard":
            if size and size == "1024x1024":
                model = "dall-e-3-1024"
            elif size and size == "1792x1024" or size and size == "1024x1792":
                model = "dall-e-3-1792"
            else:
                model = "dall-e-3-1024"
        else:
            model = "dall-e-3-1024"

    elif model and model == "dall-e-2":
        if size and size == "1024x1024":
            model = "dall-e-2-1024"
        elif size and size == "512x512":
            model = "dall-e-2-512"
        elif size and size == "256x256":
            model = "dall-e-2-256"
        else:
            model = "dall-e-2-1024"
    else:
        model = "dall-e-3-1024"

    # Verify user and her appkey
    confirm_verify = await verify_user_appkey(username, model, appkey)
    if confirm_verify["status_code"] != status.HTTP_200_OK:
        return confirm_verify

    # Collect data
    description = {
        "username": username,
        "user_content": user_content,
    }

    if model:
        description["model"] = model
    if size:
        description["size"] = size
    if quality:
        description["quality"] = quality
    if response_format:
        description["response_format"] = response_format
    if n:
        description["n"] = n
    if style:
        description["style"] = style

    # Working with OpenAI
    confirm_dall_e = await mod_gen_dall_e(description)

    if confirm_dall_e == "Error: There is no money for OpenAI account.":
        logging.info("There is no money for OpenAI account.")
        # Передача сигнала телеграмм боту, администратору пока что хз как соеденить их)))

    return confirm_dall_e





#### Create image variation dall-e-2:
@app.post("/api/variations-dall-e/", status_code=status.HTTP_200_OK)
async def variations_dall_e_func(
    username: str = Form(...),                      # !
    size: str = Form(None),                         # 256x256, 512x512, or 1024x1024
    response_format: str = Form(None),              # url or b64_json
    n: int = Form(None),                            # 1 and 10
    model: str = Form(None),                        # Only dall-e-2
    appkey: str = Header(...),                      # !
    file: Optional[UploadFile] = File(),            # ! PNG < 4mb square image
):

    # Check mistakes:
    if model and model != "dall-e-2":
        print("Error! Only Dalle-2 support variation image.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Only Dalle-2 support variation image.",
        )

    if size and size == "1792x1024" or size and size == "1024x1792":
        print("Error! Not support size.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support size.",
        )

    elif size and size == "1792x1024" or size and size == "1024x1792":
        print("Error! Not support size.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support size.",
        )
    
    # Choosing a price list
    if size and size == "1024x1024":
        model = "dall-e-2-1024"
    elif size and size == "512x512":
        model = "dall-e-2-512"
    elif size and size == "256x256":
        model = "dall-e-2-256"
    else:
        model = "dall-e-2-1024"

    # Verify user and her appkey
    confirm_verify = await verify_user_appkey(username, model, appkey)
    if confirm_verify["status_code"] != status.HTTP_200_OK:
        return confirm_verify

    # Save img to server
    image_path = f"./uploads/{file.filename}"
    async with aiofiles.open(image_path, "wb") as buffer:
        while content := await file.read(1024):  # Читаем файл порциями по 1024 байта
            await buffer.write(content)
    # with open(image_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)

    # Collect data
    description = {
        "username": username,
        "model": model
    }

    if size:
        description["size"] = size
    if response_format:
        description["response_format"] = response_format
    if n:
        description["n"] = n

    # Working with OpenAI
    confirm_dall_e = await variations_dall_e(description, image_path)

    # Remove file
    if image_path:
        remove = await remove_file_os(image_path)

    if confirm_dall_e == "Error: There is no money for OpenAI account.":
        logging.info("There is no money for OpenAI account.")
        # Передача сигнала телеграмм боту, администратору пока что хз как соеденить их)))

    return confirm_dall_e





#### Edits IMAGE Dall-e 2 :
@app.post("/api/edit-dall-e/", status_code=status.HTTP_200_OK)
async def edit_dall_e_point(
    username: str = Form(...),
    user_content: str = Form(...),                   # ! < 1000
    size: str = Form(None),                          # Only 256x256, 512x512, or 1024x1024
    response_format: str = Form(None),               # url or b64_json
    n: int = Form(None),                             # 1 and 10
    model: str = Form(None),                         # only Dall-e 2
    appkey: str = Header(...),
    image: Optional[UploadFile] = File(),            # ! PNG ALFA IN < 4mb square image  - Если маска не указана, изображение должно иметь прозрачность, которая будет использоваться в качестве маски.
    mask: Optional[UploadFile] = File(None)          # PNG & ALFA OUT < 4mb square image & size image = size mask - это изображение внедряется в пустое место картинки image
):

    # Check mistakes:
    if model and model != "dall-e-2":
        print("Error! Only Dalle-2 support edit image.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Only Dalle-2 support edit image.",
        )
    if len(user_content) > 1000:
        print("Error! Not support > 1000 simbol")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support > 1000 simbol",
        )
    if size and size == "1792x1024" or size and size == "1024x1792":
        print("Error! Not support size.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support size.",
        )
    
    if size and size == "1024x1024":
        model = "dall-e-2-1024"
    elif size and size == "512x512":
        model = "dall-e-2-512"
    elif size and size == "256x256":
        model = "dall-e-2-256"
    else:
        model = "dall-e-2-1024"

    # Verify user and her appkey
    confirm_verify = await verify_user_appkey(username, model, appkey)
    if confirm_verify["status_code"] != status.HTTP_200_OK:
        return confirm_verify

    # Save img to server
    image_path = f"./uploads/{image.filename}"
    async with aiofiles.open(image_path, "wb") as buffer:
        while content := await image.read(1024):  # Читаем файл порциями по 1024 байта
            await buffer.write(content)
    # with open(image_path, "wb") as buffer:
    #     shutil.copyfileobj(image.file, buffer)

    if mask:
        # Save mask to server
        mask_path = f"./uploads/{mask.filename}"
        async with aiofiles.open(mask_path, "wb") as buffer:
            while content := await mask.read(1024):  # Читаем файл порциями по 1024 байта
                await buffer.write(content)
        # with open(mask_path, "wb") as buffer:
        #     shutil.copyfileobj(mask.file, buffer)
    else:
        mask_path = None

    # Collect data
    description = {
        "username": username,
        "user_content": user_content,
    }

    if model:
        description["model"] = model
    if size:
        description["size"] = size
    if response_format:
        description["response_format"] = response_format
    if n:
        description["n"] = n

    # Working with OpenAI
    confirm_dall_e = await mod_edit_dall_e(description, image_path, mask_path)

    # Remove file
    if image_path:
        remove = await remove_file_os(image_path)
    if mask_path:
        remove = await remove_file_os(mask_path)

    if confirm_dall_e == "Error: There is no money for OpenAI account.":
        logging.info("There is no money for OpenAI account.")
        # Передача сигнала телеграмм боту, администратору пока что хз как соеденить их)))

    return confirm_dall_e










#### AUDIO ####


# Audio from the input text. OPENAI Endpoint:
@app.post("/api/speech-to-audio-openai/", status_code=status.HTTP_200_OK)
async def point_speech_to_audio_openai(
    username: str = Form(...),                      # !
    user_content: str = Form(...),                  # ! text < 4096
    voice: str = Form(None),                        # type voice: alloy, echo, fable, onyx, nova, and shimmer
    model: str = Form(None),                        # tts-1 or tts-1-hd
    response_format: str = Form(None),              # output format audio mp3, opus, aac, flac, wav, and pcm
    speed: float = Form(None),                      # speed 0.25 to 4.0. default - 1.0
    appkey: str = Header(...),                      # !
):

    # Choosing a price list.
    if not model:
        model = "tts-1"

    # Verify user and her appkey
    confirm_verify = await verify_user_appkey(username, model, appkey)
    if confirm_verify["status_code"] != status.HTTP_200_OK:
        return confirm_verify

    # Collect data
    description = {
        "username": username,
        "user_content": user_content,
    }
    
    if model:
        description["model"] = model
    if voice:
        description["voice"] = voice
    if response_format:
        description["response_format"] = response_format
    if speed:
        description["speed"] = speed

    # Working with OpenAI
    confirm_openai = await speech_to_audio_openai(description)


    # if confirm_openai == "Error: There is no money for OpenAI account.":
    #     logging.error("There is no money for OpenAI account.")
    #     # Передача сигнала телеграмм боту, администратору пока что хз как соеденить их)))

    encoded_string = await encode_file(confirm_openai)

    # Возвращаем результат в формате JSON
    return {"b64_json": encoded_string}






# Create transcription OPENAI Endpoint:
@app.post("/api/transcription-openai/", status_code=status.HTTP_200_OK)
async def point_transcription_openai(
    username: str = Form(...),                      # !
    language: str = Form(None),                     # input language in ISO-639-1, will improve accuracy and latency
    model: str = Form(None),                        # Only whisper-1 is free code
    response_format: str = Form(None),              # output format json, text, srt, verbose_json, or vtt.
    prompt: str = Form(None),                       # The prompt should match the audio language.
    appkey: str = Header(...),                      # !
    audio: Optional[UploadFile] = File(),           # ! flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav или webm. In Telegram ogg.
):

    # Choosing a price list.
    if not model:
        model = "whisper-1"

    # Verify user and her appkey
    confirm_verify = await verify_user_appkey(username, model, appkey)
    if confirm_verify["status_code"] != status.HTTP_200_OK:
        return confirm_verify

    # Collect data
    description = {
        "username": username,
    }
    
    if model:
        description["model"] = model
    if language:
        description["language"] = language
    if response_format:
        description["response_format"] = response_format
    if prompt:
        description["prompt"] = prompt

    if audio:
        # Save audio to server
        name = random_name_2X()
        audio_path = f"{uploads}{name}-{audio.filename}"
        async with aiofiles.open(audio_path, "wb") as buffer:
            while content := await audio.read(1024):  # Читаем файл порциями по 1024 байта
                await buffer.write(content)
        # with open(audio_path, "wb") as buffer:
        #     shutil.copyfileobj(audio.file, buffer)
    else:
        audio_path = None

    print(audio_path)

    # Working with OpenAI
    confirm_openai = await transcription_openai(description, audio_path)

    # Remove file
    if audio_path:
        remove = await remove_file_os(audio_path)

    return confirm_openai




####



























#### GEMINI ####

# TEXT & IMG GEMINI Endpoint
@app.post("/api/gemini/", status_code=status.HTTP_200_OK)
async def gemini_api(
    username: str = Form(...),
    user_content: str = Form(...),
    system_content: str = Form(None),
    model: str = Form(None),
    appkey: str = Header(...),
    file: Optional[UploadFile] = File(None)
):
    if not model:
        model = "gemini-1.5-flash-latest"

    # Verify user and her appkey
    confirm_verify = await verify_user_appkey(username, model, appkey)
    if confirm_verify["status_code"] != status.HTTP_200_OK:
        return confirm_verify

    if file:
        # Save file to server
        file_path = f"./uploads/{file.filename}"
        async with aiofiles.open(file_path, "wb") as buffer:
            while content := await file.read(1024):  # Читаем файл порциями по 1024 байта
                await buffer.write(content)
        # with open(file_path, "wb") as buffer:
        #     shutil.copyfileobj(file.file, buffer)
    else:
        file_path = None

    # Collect data
    description = {
        "username": username,
        "user_content": user_content,
        "model": model,
    }

    if system_content:
        description["system_content"] = system_content


    # Working with Gemini
    confirm_gemini = await mod_gemini(description, file_path)

    # Remove file
    if file_path:
        remove = await remove_file_os(file_path)

    return confirm_gemini
















if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) # При деплое переделать#### GEMINI TEXT ####









# # Function to translate text using OpenAI
# def translate_text(text, target_language='Spanish'):
#     response = openai.Completion.create(
#         model="text-davinci-003",  # or the latest model you want to use
#         prompt=f"Translate the following English text to {target_language}: {text}",
#         max_tokens=60
#     )
#     return response.choices[0].text.strip()





































# # Model Gemini Text
# class UserInput_Gemini(BaseModel):
#     user_content: str
#     #system_content: str
#     system_content: Optional[str] = None
#     username: str
#     model: str
#     #tools: str
#     tools: Optional[str] = None

# # TEXT GEMINI Endpoint
# @app.post("/api/gemini/", status_code=status.HTTP_200_OK)
# async def gemini_api(user_input: UserInput_Gemini, appkey: str = Header(...)):

#     # Verify user and her appkey
#     username = user_input.username
#     model = user_input.model
#     confirm_verify = await verify_user_appkey(username, model, appkey)
#     if confirm_verify["status_code"] != status.HTTP_200_OK:
#         raise

#     # Working with Gemini
#     confirm_gemini = await mod_gemini(username, user_input)


#     return confirm_gemini