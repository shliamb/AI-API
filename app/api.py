import logging
logging.basicConfig(level=logging.INFO, filename='./log/api.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл
# Base
import asyncio
import aiofiles
# from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone, timedelta
# import os
# import shutil
# import requests
# Fasapi
from fastapi import FastAPI, HTTPException, Request, Header, Depends, status, UploadFile, File, Form
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from collections import defaultdict
import uvicorn
# import gunicorn
# Service
from worker_db import get_user_by_username, update_user
from general_functions import day_utcnow, unformat_date, remove_file_os, random_name_2X, encode_file
from mod_openai_main import mod_openai_text_img
from mod_gemini_main import mod_gemini
from mod_claude_main import mod_claude
from mod_grok_main import mod_grok
from mod_openai_gen_img import mod_gen_dall_e
from mod_openai_text_to_audio import speech_to_audio_openai
from mod_openai_transcription import transcription_openai
from mod_openai_translation import translation_openai
from mod_openai_quick_assist import oa_asist_custom_0525, oa_assist_retrieve, oa_assist_list, oa_assist_del, oa_thread_del, oa_returning_result_assist
from config import LIMIT_TRY, TIME_OUT_ERR_USERNAME, WAITING_TIME, PRICE, UPLOADS, DEF_MOD_GOOGLE, DEF_MOD_OPENAI, DEF_MOD_CLAUDE, TIME_WINDOW, REQUEST_LIMIT, DEF_MOD_GROK, USERNAME_ADMIN


app = FastAPI()




# Protection from poking
ip_request_counts = defaultdict(list)
lock = asyncio.Lock() # "Creating" (Создание) lock.

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    ip = request.client.host
    now = datetime.now()
    time_window_start = now - timedelta(seconds=TIME_WINDOW)

    async with lock: # "Acquiring" (Получение) lock.
        ip_request_counts[ip] = [t for t in ip_request_counts[ip] if t > time_window_start]
        ip_request_counts[ip].append(now)
        request_count = len(ip_request_counts[ip])

    if request_count > REQUEST_LIMIT:
        logging.error(f"Rate limit exceeded for IP: {ip}")
        return Response(status_code=429, content="Too Many Requests")

    response = await call_next(request)
    return response



# USER VERIFICATION:
async def verify_user_appkey(username: str, model: str, appkey: str):
    data_by_username = await get_user_by_username(username)
    
    if data_by_username is None:
        await asyncio.sleep(TIME_OUT_ERR_USERNAME)
        logging.error("Invalid UserName in Body! After a failed attempt, a 5-second wait is activated.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid UserName in Body! After a failed attempt, a 5-second wait is activated. To register - https://t.me/myapi_aibot",
        )

    if data_by_username.is_block is True:

        un_waiting_time = float(0.01 * float(WAITING_TIME))

        date_now = await day_utcnow()
        un_date_now = await unformat_date(date_now)
        un_date_block = await unformat_date(data_by_username.date_block)
        un_time = un_date_now[1] - un_date_block[1]

        if un_date_now[0] == un_date_block[0] and un_time < un_waiting_time:
            logging.error(f"Sorry, the user is blocked for {WAITING_TIME} minutes, after {LIMIT_TRY} unsuccessful attempts.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Sorry, the user is blocked for {WAITING_TIME} minutes, after {LIMIT_TRY} unsuccessful attempts.",
            )
        
        if un_date_now[0] != un_date_block[0] or un_time >= un_waiting_time:
            updated_data = {"is_block": False, "is_failed": 0}
            await update_user(data_by_username.id, updated_data)
            logging.error("Congratulations! The time for blocking the user has passed, try again to access the API with the correct data.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Congratulations! The time for blocking the user has passed, try again to access the API with the correct data.",
            )

    if appkey != str(data_by_username.appkey) and data_by_username.is_failed < LIMIT_TRY:
        new_limit = data_by_username.is_failed + 1
        updated_data = {"is_failed": new_limit}
        await update_user(data_by_username.id, updated_data)
        logging.error(f"Invalid API Key, {new_limit} attempt out of {LIMIT_TRY}.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid API Key, {new_limit} attempt out of {LIMIT_TRY}.",
        )
    
    if appkey != str(data_by_username.appkey) and data_by_username.is_failed >= LIMIT_TRY:
        updated_data = {"is_block": True, "date_block":  await day_utcnow() } 
        await update_user(data_by_username.id, updated_data)
        logging.error(f"Invalid API Key, valid attempts have ended, sorry, try again in {WAITING_TIME} minutes.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid API Key, valid attempts have ended, sorry, try again in {WAITING_TIME} minutes.",
        )

    if data_by_username.money <= 0:
        logging.error("Insufficient funds. Please add funds to your account.")
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient funds. Please add funds to your account.",
        )

    if model not in PRICE:
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
    appkey: str = Header(...),                      # !
    assist_content: str = Form(None),               # history
    response_format: str = Form(None),              # Json response rules if need this, text or json
    user_content: str = Form(...),                  # !
    system_content: str = Form(None),               #
    model: str = Form(None),                        #
    image: Optional[UploadFile] = File(None)        # # jpg, png проверенно   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! file !!!!!!!!!!!!!!!!!!!!!!!
):
    
    try:
        assist_content = json.loads(assist_content) # Из Json (str) в dict
    except:
        print("INFO:     assist_content is str. OpenAI.")

    try:
        response_format = json.loads(response_format) # Из Json (str) в dict
    except:
        print("INFO:     response_format is str. OpenAI.")

    # Choosing a price list.
    if not model:
        model = DEF_MOD_OPENAI

    # Verify user and her appkey
    confirm_verify = await verify_user_appkey(username, model, appkey)
    if confirm_verify["status_code"] != status.HTTP_200_OK:
        return confirm_verify

    if image:
        # Save img to server
        name = random_name_2X()
        image_path = f"{UPLOADS}{name}-{image.filename}"
        async with aiofiles.open(image_path, "wb") as buffer:
            while content := await image.read(1024):  # Читаем файл порциями по 1024 байта
                await buffer.write(content)
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
    if assist_content:
        description["assist_content"] = assist_content
    if response_format:
        description["response_format"] = response_format

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


    print("HIIII")
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
        audio_path = f"{UPLOADS}{name}-{audio.filename}" # ./UPLOADS/I34-t47-in_audio_2.ogg
        async with aiofiles.open(audio_path, "wb") as buffer:
            while content := await audio.read(1024):  # Читаем файл порциями по 1024 байта
                await buffer.write(content)
        # with open(audio_path, "wb") as buffer:
        #     shutil.copyfileobj(audio.file, buffer)
    else:
        audio_path = None

    # Working with OpenAI
    confirm_openai = await transcription_openai(description, audio_path)
    print(confirm_openai)

    # Remove file
    if audio_path:
        remove = await remove_file_os(audio_path)

    return confirm_openai






# Create translation into English OPENAI Endpoint:
@app.post("/api/translation-openai/", status_code=status.HTTP_200_OK)
async def point_translation_openai(
    username: str = Form(...),                      # !
    model: str = Form(None),                        # Only whisper-1 is free code
    response_format: str = Form(None),              # output format json, text, srt, verbose_json, or vtt.
    prompt: str = Form(None),                       # in English
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
    if response_format:
        description["response_format"] = response_format
    if prompt:
        description["prompt"] = prompt

    if audio:
        # Save audio to server
        name = random_name_2X()
        audio_path = f"{UPLOADS}{name}-{audio.filename}" # ./UPLOADS/I34-t47-in_audio_2.ogg
        async with aiofiles.open(audio_path, "wb") as buffer:
            while content := await audio.read(1024):  # Читаем файл порциями по 1024 байта
                await buffer.write(content)
    else:
        audio_path = None

    # Working with OpenAI
    confirm_openai = await translation_openai(description, audio_path)

    # Remove file
    if audio_path:
        remove = await remove_file_os(audio_path)

    return confirm_openai




#### Assistants OpenAI: ####
# В идеале, позже провести рекодинг по этому примеру или лучше..
# Siple Assistent OpenAI:
@app.post("/api/oa-assist-custom-0525/", status_code=status.HTTP_200_OK)
async def in_oa_assist_custom_0525(
    username: str = Form(...),
    appkey: str = Header(...),
    name: Optional[str] = Form(None),
    instructions: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    user_content: Optional[str] = Form(None),        
    tools: Optional[str] = Form(None),
    assistant_id: Optional[str] = Form(None),
    thread_id: Optional[str] = Form(None)
):
    '''
    Упрощённый endpoint, объединяющий несколько задач OpenAI Assistant.  
    Если переданы assistant_id и thread_id, подключается к существующему ассистенту и диалогу.  
    Если они отсутствуют — создаёт нового ассистента и диалог.  
    При наличии user_content, отправляет сообщение в thread и запускает выполнение.  
    Возвращает:  
    - assistant_id, thread_id, run_id — если передано user_content,  
    - только assistant_id и thread_id — если контент отсутствует.
    '''

    if username != USERNAME_ADMIN:
        error_msg = f"Access denied for user '{username}'"
        logging.error(error_msg)
        return error_msg

    # Verify user and their appkey (подтверждение авторизации):
    verification = await verify_user_appkey(username, model, appkey)
    if verification.get("status_code") != status.HTTP_200_OK:
        logging.error("User verification failed: %s", verification)
        return verification

    # Сбор данных запроса в один dict: 
    data = {
        "name": name,
        "instructions": instructions,
        "model": model or DEF_MOD_OPENAI,
        "user_content": user_content,
        "tools": tools,
        "assistant_id": assistant_id,
        "thread_id": thread_id
    }

    return await oa_asist_custom_0525(data)



# Getting a response from an active assistant:
@app.post("/api/oa-assist-retrieve/", status_code=status.HTTP_200_OK)
async def in_oa_assist_retrieve(
    username: str = Form(...),
    appkey: str = Header(...),
    run_id: str = Form(...),
    thread_id: str = Form(...)
):

    '''Получение ответа от активного ассистента по указанному каналу (thread_id) и идентификатору запуска (run_id).'''

    if username != USERNAME_ADMIN:
        error_msg = f"Access denied for user '{username}'"
        logging.error(error_msg)
        return error_msg

    model = "assistent-oa" # Пока что не знаю как и че делать с этим..

    # Verify user and their appkey (подтверждение авторизации):
    verification = await verify_user_appkey(username, model, appkey)
    if verification.get("status_code") != status.HTTP_200_OK:
        logging.error("User verification failed: %s", verification)
        return verification


    return await oa_assist_retrieve(run_id, thread_id)



# Получение списка Асистентов:
@app.post("/api/oa-assist-list/", status_code=status.HTTP_200_OK)
async def in_oa_assist_list(
    username: str = Form(...),
    appkey: str = Header(...)
):

    '''Получение списка агентов'''

    if username != USERNAME_ADMIN:
        error_msg = f"Access denied for user '{username}'"
        logging.error(error_msg)
        return error_msg

    model = "assistent-oa" # Пока что не знаю как и че делать с этим..

    # Verify user and their appkey (подтверждение авторизации):
    verification = await verify_user_appkey(username, model, appkey)
    if verification.get("status_code") != status.HTTP_200_OK:
        logging.error("User verification failed: %s", verification)
        return verification

    return await oa_assist_list()



# Удаление ассистента:
@app.post("/api/oa-assist-del/", status_code=status.HTTP_200_OK)
async def in_oa_assist_del(
    username: str = Form(...),
    appkey: str = Header(...),
    assistant_id: str = Form(...)
):

    '''Удаление Ассистента'''

    if username != USERNAME_ADMIN:
        error_msg = f"Access denied for user '{username}'"
        logging.error(error_msg)
        return error_msg

    model = "assistent-oa" # Пока что не знаю как и че делать с этим..

    # Verify user and their appkey (подтверждение авторизации):
    verification = await verify_user_appkey(username, model, appkey)
    if verification.get("status_code") != status.HTTP_200_OK:
        logging.error("User verification failed: %s", verification)
        return verification
    
    return await oa_assist_del(assistant_id)




# Удаление Thread:
@app.post("/api/oa-thread-del/", status_code=status.HTTP_200_OK)
async def in_oa_thread_del(
    username: str = Form(...),
    appkey: str = Header(...),
    thread_id: str = Form(...)
):

    '''Удаление Thread'''

    if username != USERNAME_ADMIN:
        error_msg = f"Access denied for user '{username}'"
        logging.error(error_msg)
        return error_msg

    model = "assistent-oa" # Пока что не знаю как и че делать с этим..

    # Verify user and their appkey (подтверждение авторизации):
    verification = await verify_user_appkey(username, model, appkey)
    if verification.get("status_code") != status.HTTP_200_OK:
        logging.error("User verification failed: %s", verification)
        return verification
    
    return await oa_thread_del(thread_id)




# Возврат результата Агенту:
@app.post("/api/oa-return-result-assist/", status_code=status.HTTP_200_OK)
async def in_oa_thread_del(
    username: str = Form(...),
    appkey: str = Header(...),
    run_id: str = Form(...),
    thread_id: str = Form(...),
    tool_outputs: str = Form(...)
):

    '''Возврат результата Агенту'''

    if username != USERNAME_ADMIN:
        error_msg = f"Access denied for user '{username}'"
        logging.error(error_msg)
        return error_msg

    model = "assistent-oa" # Пока что не знаю как и че делать с этим..

    # Verify user and their appkey (подтверждение авторизации):
    verification = await verify_user_appkey(username, model, appkey)
    if verification.get("status_code") != status.HTTP_200_OK:
        logging.error("User verification failed: %s", verification)
        return verification
    
    return await oa_returning_result_assist(run_id, thread_id, tool_outputs)













#### GEMINI ####

# TEXT & IMG GEMINI Endpoint
@app.post("/api/gemini/", status_code=status.HTTP_200_OK)
async def gemini_api(
    username: str = Form(...),
    appkey: str = Header(...),
    assist_content: str = Form(None),               # history
    response_format: str = Form(None),              # Json response rules if need this, text or json
    user_content: str = Form(...),                  # !
    system_content: str = Form(None),
    model: str = Form(None),
    file: Optional[UploadFile] = File(None),
):
    try:
        assist_content = json.loads(assist_content) # Из Json (str) в dict
    except:
        print("INFO:     assist_content is str. Gemini.")

    try:
        response_format = json.loads(response_format) # Из Json (str) в dict
    except:
        print("INFO:     response_format is str. Gemini.")

    # Choosing a price list.
    if not model:
        model = DEF_MOD_GOOGLE

    # Verify user and her appkey
    confirm_verify = await verify_user_appkey(username, model, appkey)
    if confirm_verify["status_code"] != status.HTTP_200_OK:
        return confirm_verify

    if file:
        # Save file to server
        name = random_name_2X()
        file_path = f"{UPLOADS}{name}-{file.filename}"
        async with aiofiles.open(file_path, "wb") as buffer:
            while content := await file.read(1024):  # Читаем файл порциями по 1024 байта
                await buffer.write(content)
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
    if assist_content:
        description["assist_content"] = assist_content
    if response_format:
        description["response_format"] = response_format


    # Working with Gemini
    confirm_gemini = await mod_gemini(description, file_path)

    # Remove file
    if file_path:
        remove = await remove_file_os(file_path)

    return confirm_gemini






#### Claude ####

# TEXT & IMG Claude Endpoint
@app.post("/api/claude/", status_code=status.HTTP_200_OK)
async def claude_api(
    username: str = Form(...),
    appkey: str = Header(...),
    assist_content: str = Form(None),               # history
    # response_format: str = Form(None),
    user_content: str = Form(...),                  # !
    system_content: str = Form(None),
    model: str = Form(None),
    image: Optional[UploadFile] = File(None),
):
    try:
        assist_content = json.loads(assist_content) # Из Json (str) в dict
    except:
        print("INFO:     assist_content is str. Claude.")

    # try:
    #     response_format = json.loads(response_format) # Из Json (str) в dict
    # except:
    #     print("INFO:     response_format is str. Claude.")

    # Choosing a price list.
    if not model:
        model = DEF_MOD_CLAUDE

    # Verify user and her appkey
    confirm_verify = await verify_user_appkey(username, model, appkey)
    if confirm_verify["status_code"] != status.HTTP_200_OK:
        return confirm_verify

    if image:
        # Save file to server
        name = random_name_2X()
        file_path = f"{UPLOADS}{name}-{image.filename}"
        async with aiofiles.open(file_path, "wb") as buffer:
            while content := await image.read(1024):  # Читаем файл порциями по 1024 байта
                await buffer.write(content)
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
    if assist_content:
        description["assist_content"] = assist_content
    # if response_format:
    #     description["response_format"] = response_format


    # Working with Claude
    confirm_claude = await mod_claude(description, file_path)

    # Remove file
    if file_path:
        remove = await remove_file_os(file_path)

    return confirm_claude







#### Elon Musk Grok ####

# TEXT & IMG Elon Musk Grok Endpoint
@app.post("/api/grok/", status_code=status.HTTP_200_OK)
async def grok_api(
    username: str = Form(...),
    appkey: str = Header(...),
    assist_content: str = Form(None),               # history
    # response_format: str = Form(None),
    user_content: str = Form(...),                  # !
    system_content: str = Form(None),
    model: str = Form(None),
    image: Optional[UploadFile] = File(None),
):
    try:
        assist_content = json.loads(assist_content) # Из Json (str) в dict
    except:
        print("INFO:     assist_content is str. Grok.")

    # try:
    #     response_format = json.loads(response_format) # Из Json (str) в dict
    # except:
    #     print("INFO:     response_format is str. Grok.")

    # Choosing a price list.
    if not model:
        model = DEF_MOD_GROK

    # Verify user and her appkey
    confirm_verify = await verify_user_appkey(username, model, appkey)
    if confirm_verify["status_code"] != status.HTTP_200_OK:
        return confirm_verify

    if image:
        # Save file to server
        name = random_name_2X()
        file_path = f"{UPLOADS}{name}-{image.filename}"
        async with aiofiles.open(file_path, "wb") as buffer:
            while content := await image.read(1024):  # Читаем файл порциями по 1024 байта
                await buffer.write(content)
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
    if assist_content:
        description["assist_content"] = assist_content
    # if response_format:
    #     description["response_format"] = response_format


    # Working with Grok
    confirm_grok = await mod_grok(description, file_path)

    # Remove file
    if file_path:
        remove = await remove_file_os(file_path)

    return confirm_grok








if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)







































