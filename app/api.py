from config import UPLOADS, DEF_MOD_GOOGLE, DEF_MOD_OPENAI, DEF_MOD_CLAUDE, TIME_WINDOW, REQUEST_LIMIT, DEF_MOD_GROK, ALLOWED_HEADER_NAMES, SUPER_HEADER_NAMES, MAX_DEQUE_LEN #, TIME_OUT_ERR_USERNAME, WAITING_TIME, LIMIT_TRY, PRICE, USERNAME_ADMIN

from setup_config_logger import setup_logger
logger_api = setup_logger('api', '/log/api.log')

import asyncio
import aiofiles
import json
from typing import Optional, Dict, List, Union, Deque #, List
import uuid
import time
from datetime import datetime, timedelta #, timezone
from collections import defaultdict, deque
from contextlib import asynccontextmanager
import urllib.parse
# import os
# import shutil
# import requests
# from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request, Response, status, UploadFile, File, Form, Depends #, Header
from fastapi.responses import Response #, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# import gunicorn
from worker_db import read_account_access_id, read_user
from general_functions import DictObj, random_name, remove_file_os, encode_file #, day_utcnow, unformat_date, random_name_2X, encode_file
from mod_openai_main import openai_text
from mod_openai_img import openai_img
from mod_openai_text_to_voice import openai_text_to_voice
from mod_openai_voice_to_text import openai_voice_to_text
from mod_gemini_main import gemini_text
from mod_claude_main import claude_text
from mod_grok_main import grok_text
# from mod_openai_quick_assist import oa_asist_custom_0525, oa_assist_retrieve, oa_assist_list, oa_assist_del, oa_thread_del, oa_returning_result_assist




app = FastAPI()

PARANOIA_MODE = False






# Конфигурация CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],  # Только нужные методы "GET", "POST", "PUT", "DELETE"
    allow_headers=["*"]
)



'''
1. **Класс RateLimiter** - инкапсуляция логики
2. **time.time()** вместо datetime - быстрее
3. **Очистка памяти** - автоматическое удаление старых IP
4. **Реальный IP** - учет прокси и балансировщиков
5. **Retry-After заголовок** - информирует клиента о времени ожидания
6. **Фоновая очистка** - предотвращает утечки памяти
'''


# Rate limiting
class RateLimiter:
    def __init__(self, request_limit: int = REQUEST_LIMIT, time_window: int = TIME_WINDOW):
        self.request_limit = request_limit
        self.time_window = time_window
        self.ip_requests: Dict[str, List[float]] = defaultdict(list)
        self.lock = asyncio.Lock()
    
    async def is_allowed(self, ip: str) -> bool:
        now = time.time()
        cutoff = now - self.time_window
        
        async with self.lock:
            # Очистка старых записей
            self.ip_requests[ip] = [t for t in self.ip_requests[ip] if t > cutoff]
            
            if len(self.ip_requests[ip]) >= self.request_limit:
                return False
            
            self.ip_requests[ip].append(now)
            return True
    
    async def cleanup_old_ips(self):
        """Периодическая очистка неактивных IP"""
        now = time.time()
        cutoff = now - self.time_window * 2
        
        async with self.lock:
            inactive_ips = [
                ip for ip, timestamps in self.ip_requests.items()
                if not timestamps or max(timestamps) < cutoff
            ]
            for ip in inactive_ips:
                del self.ip_requests[ip]



rate_limiter = RateLimiter()

@app.middleware("http")
async def combined_middleware(request: Request, call_next):
    # Получение реального IP
    ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    if not ip:
        ip = request.headers.get("X-Real-IP", "")
    if not ip:
        ip = request.client.host
    
    # Rate limiting
    if not await rate_limiter.is_allowed(ip):
        logger_api.warning(f"Rate limit exceeded for IP: {ip}")
        return Response(
            status_code=429, 
            content="Rate limit exceeded. Try again later.",
            headers={"Retry-After": str(TIME_WINDOW)}
        )
    
    # Получаем body один раз
    body = await request.body()
    
    # Декодируем для логов
    if body:
        try:
            decoded_body = urllib.parse.unquote_plus(body.decode('utf-8'))
            if len(decoded_body) > 200:
                decoded_body = decoded_body[:200] + "..."
        except:
            decoded_body = body.decode('utf-8', errors='ignore')[:200]
    else:
        decoded_body = ""
    
    # Логируем
    logger_api.info(f"{ip} -> {request.method} {request.url.path} | {decoded_body}")
    
    # Пересоздаем request
    async def receive():
        return {"type": "http.request", "body": body}
    
    request._receive = receive
    
    response = await call_next(request)
    return response

# Порядок выполнения:
# 1. Получение IP
# 2. Проверка rate limit (если превышен - возврат 429 без логирования)
# 3. Чтение body
# 4. Логирование запроса
# 5. Выполнение основного обработчика



# Фоновая задача для очистки
@asynccontextmanager
async def lifespan(app):
    # Запуск
    cleanup_task = asyncio.create_task(periodic_cleanup())
    yield
    # Остановка
    cleanup_task.cancel()

async def periodic_cleanup():
    while True:
        await asyncio.sleep(TIME_WINDOW * 2)
        await rate_limiter.cleanup_old_ips()

app.router.lifespan_context = lifespan











#############

# Parsing JSON content:
async def parse_json_content(content: str) -> Union[str, dict]:
    try:
        return json.loads(content)
    except (json.JSONDecodeError, TypeError) as e:
        return content



# Checking if UUID is valid:
async def verify_uuid(some: str) -> bool:
    try:
        some = str(some) if some else None
        uuid_obj = uuid.UUID(some, version=4)
        return str(uuid_obj) == some
    except:
        logger_api.error(f"Error: Invalid API Name Key format: {some}")
        return False


# Checking API user access:
async def verify_user(access_id: uuid, appkey: uuid) -> bool:

    # Get user data from database using access_id:
    data_access_user = await read_account_access_id(access_id)

    # If no accounts found:
    if not data_access_user:
        logger_api.error(f"Error: Invalid Access ID API: {access_id}")
        return False
    
    data_access = DictObj(data_access_user)
    
    # Check the key value:
    if str(data_access.api_value) != appkey:
        logger_api.error(f"Error: Invalid Access ID or API Value: {access_id} | {appkey}")
        return False
    
    # Get Telegram user data:
    data_user = await read_user(data_access.user_id_telegram)
    data_user = DictObj(data_user)

    # Check user balance:
    if data_user.money <= 0 :
        logger_api.error(f"Error: Don't have money: {access_id} | {appkey}")
        return False

    # Check if user is blocked:
    if data_user.block_user:
        logger_api.error(f"Error: User has blocked: {access_id} | {appkey}")
        return False
    
    return True


# Checking Authorization Name for API:
async def verify_appkey(request: Request) -> str:
    received_key = None

    # Check authorization names from allowed list:
    for header_name in ALLOWED_HEADER_NAMES:
        if header_name in request.headers:
            received_key = request.headers[header_name]
            break

    # Validate UUID:
    if not await verify_uuid(received_key):
        logger_api.error(f"Invalid API Name format: {received_key}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid API Name format")

    # In paranoia mode, only super users can access:
    if PARANOIA_MODE == True and header_name != SUPER_HEADER_NAMES:
        logger_api.info(f"Temporary issue – we're working on it! : {header_name}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Temporary issue – we're working on it!")

    # In normal mode, rejects invalid names:
    elif not received_key:
        logger_api.error(f"Missing or invalid API Name header: {received_key}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing or invalid API Name header")

    return received_key



############









#### OPEN AI ####
#################

# TEXT & IMAGE OPENAI Endpoint:
@app.post("/api/openai-chat/", status_code=status.HTTP_200_OK)
async def openai_api(
    access_id: uuid.UUID = Form(...),
    appkey: uuid.UUID = Depends(verify_appkey),
    user_content: str = Form(...),
    assist_content: str = Form(None),
    response_format: str = Form(None),
    system_content: str = Form(None),
    model: str = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """Endpoint for proxying requests to OpenAI chat API."""
    # Authentication and authorization
    if not await verify_user(access_id, appkey):
        logger_api.error("Wrong Access ID, API Key, or no money, or just blocked)")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Access ID, API Key, or no money, or just blocked)")
    
    # logger_api
    logger_api.info(f"{access_id} -> proxy API: 'openai-chat'")
    print(f"INFO: {access_id} -> proxy API: 'openai-chat'")

    # Parse optional JSON content
    parsed_assist_content = await parse_json_content(assist_content) if assist_content else None
    parsed_response_format = await parse_json_content(response_format) if response_format else None

    # Handle file upload if present
    file_path = f"{UPLOADS}{random_name()}-{file.filename}" if file else None
    if file_path:
        async with aiofiles.open(file_path, "wb") as buffer:
            while content := await file.read(1024): # Читаем файл порциями по 1024 байта
                await buffer.write(content)

    # Prepare request description
    description = {
        "access_id": access_id,
        "user_content": user_content,
        "model": model or DEF_MOD_OPENAI,
        "system_content": system_content,
        "assist_content": parsed_assist_content,
        "response_format": parsed_response_format,
        "file_path": file_path
    }

    try:
        answer = await openai_text(description)
    except:
        answer = "Error: mod_openai dont response"
        logger_api.error(answer)
    finally:
        if file_path and not await remove_file_os(file_path):
            logger_api.error(f"Failed to remove file - {file_path}")

    return answer







#Create image DALL-E Endpoint:
@app.post("/api/openai-img/", status_code=status.HTTP_200_OK)
async def dall_e_point(
    access_id: uuid.UUID = Form(...),
    appkey: uuid.UUID = Depends(verify_appkey),
    user_content: str = Form(...),              # !  dall-e-3 < 4000 and  dall-e-2 < 1000
    size: str = Form(None),                     # 1792 Only dall-e-3 and  512, 256 only dall-e-2
    quality: str = Form(None),                  # Only dall-e-3 support hd, standard
    response_format: str = Form(None),          # url or b64_json
    n: int = Form(None),                        # dall-e-3 only 1 and dall-e-2 1 - 10
    style: str = Form(None),                    # Only dall-e-3 support vivid ore natural
    model: str = Form(None)
):
    """Endpoint for proxying requests to OpenAI generate image API."""
    # Authentication and authorization
    if not await verify_user(access_id, appkey):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Access ID, API Key, or no money, or just blocked)")
    
    # logger_api
    logger_api.info(f"{access_id} -> proxy API: 'openai-img'")
    print(f"INFO: {access_id} -> proxy API: 'openai-img'")
    
    # Check mistakes:
    if len(user_content) > 4000 and model == "dall-e-3":
        logger_api.error("Error! Not support > 4000 simbol")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support > 4000 simbol",
        )

    if len(user_content) > 1000 and model == "dall-e-2":
        logger_api.error("Error! Not support > 1000 simbols dall-e-2")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support > 1000 simbols dall-e-2",
        )

    if quality and model == "dall-e-2":
        logger_api.error("Error! Not support quality dall-e-2.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support quality dall-e-2.",
        )

    if size and size == "1792x1024" and model == "dall-e-2":
        logger_api.error("Error! Not support 1792x1024 to dall-e-2.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support 1792x1024 to dall-e-2.",
        )

    if size and size == "1024x1792" and model == "dall-e-2":
        logger_api.error("Error! Not support 1024x1792 to dall-e-2.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Not support 1024x1792 to dall-e-2.",
        )

    if model == "dall-e-3":
        if size and size == "256x256" or size and size == "512x512":
            logger_api.error("Error! Not support 512x512 and 256x256 to dall-e-3.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error! Not support 512x512 and 256x256 to dall-e-3.",
            )
        if n and n > 1:
            logger_api.error("Error! Not support n > 1 to dall-e-3.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error! Not support n > 1 to dall-e-3.",
            )
        
    if model == "dall-e-2":
        if n and n > 10:
            logger_api.error("Error! Not support n > 10 to dall-e-2.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error! Not support n > 10 to dall-e-2.",
            )
        if style:
            logger_api.error("Error! Not support style to dall-e-2.")
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

    # Prepare request description
    description = {
        "access_id": access_id,
        "user_content": user_content,
        "model": model,
        "size": size,
        "quality": quality,
        "response_format": response_format,
        "n": n,
        "style": style
    }

    try:
        answer_img = await openai_img(description)
    except:
        answer_img = "Error: mod_openai_img dont response"
        logger_api.error(answer_img)

    return answer_img








#### AUDIO ####


# OpenAI - text in voice
@app.post("/api/openai-text-to-voice/", status_code=status.HTTP_200_OK)
async def point_speech_to_audio_openai(
    access_id: uuid.UUID = Form(...),
    appkey: uuid.UUID = Depends(verify_appkey),
    user_content: str = Form(...),                  # ! text < 4096
    voice: str = Form(None),                        # type voice: alloy, echo, fable, onyx, nova, and shimmer
    model: str = Form(None),                        # tts-1 or tts-1-hd or gpt-4o-mini-tts
    response_format: str = Form(None),              # output format audio mp3, opus, aac, flac, wav, and pcm
    speed: float = Form(None)                       # speed 0.25 to 4.0. default - 1.0
):
    """Endpoint for proxying requests to OpenAI text to audio API."""
    # Authentication and authorization
    if not await verify_user(access_id, appkey):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Access ID, API Key, or no money, or just blocked)")
    
    # logger_api
    logger_api.info(f"{access_id} -> proxy API: 'openai-text-to-voice'")
    print(f"INFO: {access_id} -> proxy API: 'openai-text-to-voice'")

    # Prepare request description
    description = {
        "access_id": access_id,
        "user_content": user_content,
        "model": model or "gpt-4o-mini-tts",
        "voice": voice,
        "response_format": response_format,
        "speed": speed
    }

    file_path = None
    try:
        file_path = await openai_text_to_voice(description)
        encoded_file = await encode_file(file_path)
        return {"b64_json": encoded_file}
    
    except Exception as e:
        logger_api.error(f"Error in voice processing: {str(e)}", exc_info=True)
        #print(f"Error in voice processing: {str(e)}")
        return {"system": f"Error in voice processing openai_text_to_voice: {str(e)}"}

    finally:
        if file_path and not await remove_file_os(file_path):
            #print(f"Failed to remove file - {file_path}")
            logger_api.error(f"Failed to remove file - {file_path}")







# OpenAI - Voice To Text:
@app.post("/api/openai-voice-to-text/", status_code=status.HTTP_200_OK)
async def point_transcription_openai(
    access_id: uuid.UUID = Form(...),
    appkey: uuid.UUID = Depends(verify_appkey),
    language: str = Form(None),                     # input language in ISO-639-1, will improve accuracy and latency
    model: str = Form(None),                        # Only whisper-1 is free code
    response_format: str = Form(None),              # output format json, text, srt, verbose_json, or vtt.
    prompt: str = Form(None),                       # The prompt should match the audio language.
    file: Optional[UploadFile] = File(),           # ! flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav или webm. In Telegram ogg.
):
    """Endpoint for proxying requests to OpenAI voice to text API."""
    # Authentication and authorization
    if not await verify_user(access_id, appkey):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Access ID, API Key, or no money, or just blocked)")
    
    # logger_api
    logger_api.info(f"{access_id} -> proxy API: 'openai-voice-to-text'")
    print(f"INFO: {access_id} -> proxy API: 'openai-voice-to-text'")

    # Handle file upload if present
    file_path = f"{UPLOADS}{random_name()}-voice-{file.filename}" if file else None # ./UPLOADS/I34-t47-in_audio_2.ogg
    if file_path:
        async with aiofiles.open(file_path, "wb") as buffer:
            while content := await file.read(1024): # Читаем файл порциями по 1024 байта
                await buffer.write(content)

    # Prepare request description
    description = {
        "access_id": access_id,
        "language": language,
        "model": model or "whisper-1",
        "response_format": response_format,
        "prompt": prompt,
        "file_path": file_path
    }

    try:
        answer_text = await openai_voice_to_text(description)
    except:
        answer_text = "Error: mod_openai openai-voice-to-text dont response"
        logger_api.error(answer_text)
    finally:
        if file_path and not await remove_file_os(file_path):
            logger_api.error(f"Failed to remove file - {file_path}")

    return answer_text













#### GEMINI ####

# TEXT & IMG GEMINI Endpoint
@app.post("/api/gemini/", status_code=status.HTTP_200_OK)
async def gemini_api(
    access_id: uuid.UUID = Form(...),
    appkey: uuid.UUID = Depends(verify_appkey),
    user_content: str = Form(...),                  # !
    assist_content: str = Form(None),               # history
    response_format: str = Form(None),              # Json response rules if need this, text or json
    system_content: str = Form(None),
    model: str = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """Endpoint for proxying requests to Gemini API."""
    # Authentication and authorization
    if not await verify_user(access_id, appkey):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Access ID, API Key, or no money, or just blocked)")
    
    # logger_api
    logger_api.info(f"{access_id} -> proxy API: 'gemini'")
    print(f"INFO: {access_id} -> proxy API: 'gemini'")

    # Parse optional JSON content
    parsed_assist_content = await parse_json_content(assist_content) if assist_content else None
    parsed_response_format = await parse_json_content(response_format) if response_format else None

    # Handle file upload if present
    file_path = f"{UPLOADS}{random_name()}-{file.filename}" if file else None
    if file_path:
        async with aiofiles.open(file_path, "wb") as buffer:
            while content := await file.read(1024): # Читаем файл порциями по 1024 байта
                await buffer.write(content)

    # Prepare request description
    description = {
        "access_id": access_id,
        "user_content": user_content,
        "model": model or DEF_MOD_GOOGLE,
        "system_content": system_content,
        "assist_content": parsed_assist_content,
        "response_format": parsed_response_format,
        "file_path": file_path
    }

    try:
        answer = await gemini_text(description)
    except:
        answer = "Error: mod_gemini dont response"
        logger_api.error(answer)
    finally:
        if file_path and not await remove_file_os(file_path):
            logger_api.error(f"Failed to remove file - {file_path}")

    return answer






#### Claude ####

# TEXT & IMG Claude Endpoint
@app.post("/api/claude/", status_code=status.HTTP_200_OK)
async def claude_api(
    access_id: uuid.UUID = Form(...),
    appkey: uuid.UUID = Depends(verify_appkey),
    user_content: str = Form(...),
    assist_content: str = Form(None),
    # response_format: str = Form(None),
    system_content: str = Form(None),
    model: str = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """Endpoint for proxying requests to Claude API."""
    # Authentication and authorization
    if not await verify_user(access_id, appkey):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Access ID, API Key, or no money, or just blocked)")
    
    # logger_api
    logger_api.info(f"{access_id} -> proxy API: 'claude'")
    print(f"INFO: {access_id} -> proxy API: 'claude'")

    # Parse optional JSON content
    parsed_assist_content = await parse_json_content(assist_content) if assist_content else None
    #parsed_response_format = await parse_json_content(response_format) if response_format else None

    # Handle file upload if present
    file_path = f"{UPLOADS}{random_name()}-{file.filename}" if file else None
    if file_path:
        async with aiofiles.open(file_path, "wb") as buffer:
            while content := await file.read(1024): # Читаем файл порциями по 1024 байта
                await buffer.write(content)

    # Prepare request description
    description = {
        "access_id": access_id,
        "user_content": user_content,
        "model": model or DEF_MOD_CLAUDE,
        "system_content": system_content,
        "assist_content": parsed_assist_content,
        #"response_format": parsed_response_format,
        "file_path": file_path
    } 

    try:
        answer = await claude_text(description)
    except:
        answer = "Error: mod_claude dont response"
        logger_api.error(answer)
    finally:
        if file_path and not await remove_file_os(file_path):
            logger_api.error(f"Failed to remove file - {file_path}")

    return answer








#### Elon Musk Grok ####

# TEXT & IMG Elon Musk Grok Endpoint
@app.post("/api/grok/", status_code=status.HTTP_200_OK)
async def grok_api(
    access_id: uuid.UUID = Form(...),
    appkey: uuid.UUID = Depends(verify_appkey),
    user_content: str = Form(...),
    assist_content: str = Form(None),
    # response_format: str = Form(None),
    system_content: str = Form(None),
    model: str = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """Endpoint for proxying requests to Grok API."""
    # Authentication and authorization
    if not await verify_user(access_id, appkey):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Access ID, API Key, or no money, or just blocked)")
    
    # logger_api
    logger_api.info(f"{access_id} -> proxy API: 'Grok'")
    print(f"INFO: {access_id} -> proxy API: 'Grok'")

    # Parse optional JSON content
    parsed_assist_content = await parse_json_content(assist_content) if assist_content else None
    # parsed_response_format = await parse_json_content(response_format) if response_format else None

    # Handle file upload if present
    file_path = f"{UPLOADS}{random_name()}-{file.filename}" if file else None
    if file_path:
        async with aiofiles.open(file_path, "wb") as buffer:
            while content := await file.read(1024): # Читаем файл порциями по 1024 байта
                await buffer.write(content)

    # Prepare request description
    description = {
        "access_id": access_id,
        "user_content": user_content,
        "model": model or DEF_MOD_GROK,
        "system_content": system_content,
        "assist_content": parsed_assist_content,
        #"response_format": parsed_response_format,
        "file_path": file_path
    }

    try:
        answer = await grok_text(description)
    except:
        answer = "Error: grok_text dont response"
        logger_api.error(answer)
    finally:
        if file_path and not await remove_file_os(file_path):
            logger_api.error(f"Failed to remove file - {file_path}")

    return answer









LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(name)s %(levelname)s: %(message)s",
        },
    },
    "handlers": {
        "api_file": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./log/api.log",
            "maxBytes": 10485760,
            "backupCount": 5,
        },
        "uvicorn_file": {
            "formatter": "default", 
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./log/uvicorn.log",
            "maxBytes": 10485760,
            "backupCount": 5,
        },
    },
    "loggers": {
        "api": {"handlers": ["api_file"], "level": "INFO", "propagate": False}, 
        "uvicorn": {"handlers": ["uvicorn_file"], "level": "INFO", "propagate": False},
        "uvicorn.access": {"handlers": ["uvicorn_file"], "level": "INFO", "propagate": False},
    }
}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=LOG_CONFIG)


































    # if audio:
    #     # Save audio to server
    #     name = random_name_2X()
    #     audio_path = f"{UPLOADS}{name}-{audio.filename}" # ./UPLOADS/I34-t47-in_audio_2.ogg
    #     async with aiofiles.open(audio_path, "wb") as buffer:
    #         while content := await audio.read(1024):  # Читаем файл порциями по 1024 байта
    #             await buffer.write(content)
    #     with open(audio_path, "wb") as buffer:
    #          shutil.copyfileobj(audio.file, buffer)
    # else:
    #     audio_path = None



# #### Assistants OpenAI: ####
# # В идеале, позже провести рекодинг по этому примеру или лучше..
# # Siple Assistent OpenAI:
# @app.post("/api/oa-assist-custom-0525/", status_code=status.HTTP_200_OK)
# async def in_oa_assist_custom_0525(
#     username: str = Form(...),
#     appkey: str = Header(...),
#     name: Optional[str] = Form(None),
#     instructions: Optional[str] = Form(None),
#     model: Optional[str] = Form(None),
#     user_content: Optional[str] = Form(None),        
#     tools: Optional[str] = Form(None),
#     assistant_id: Optional[str] = Form(None),
#     thread_id: Optional[str] = Form(None)
# ):
#     '''
#     Упрощённый endpoint, объединяющий несколько задач OpenAI Assistant.  
#     Если переданы assistant_id и thread_id, подключается к существующему ассистенту и диалогу.  
#     Если они отсутствуют — создаёт нового ассистента и диалог.  
#     При наличии user_content, отправляет сообщение в thread и запускает выполнение.  
#     Возвращает:  
#     - assistant_id, thread_id, run_id — если передано user_content,  
#     - только assistant_id и thread_id — если контент отсутствует.
#     '''

#     if username != USERNAME_ADMIN:
#         error_msg = f"Access denied for user '{username}'"
#         logger_api.error(error_msg)
#         return error_msg

#     # Verify user and their appkey (подтверждение авторизации):
#     verification = await verify_user_appkey(username, model, appkey)
#     if verification.get("status_code") != status.HTTP_200_OK:
#         logger_api.error("User verification failed: %s", verification)
#         return verification

#     # Сбор данных запроса в один dict: 
#     data = {
#         "name": name,
#         "instructions": instructions,
#         "model": model or DEF_MOD_OPENAI,
#         "user_content": user_content,
#         "tools": tools,
#         "assistant_id": assistant_id,
#         "thread_id": thread_id
#     }

#     return await oa_asist_custom_0525(data)



# # Getting a response from an active assistant:
# @app.post("/api/oa-assist-retrieve/", status_code=status.HTTP_200_OK)
# async def in_oa_assist_retrieve(
#     username: str = Form(...),
#     appkey: str = Header(...),
#     run_id: str = Form(...),
#     thread_id: str = Form(...)
# ):

#     '''Получение ответа от активного ассистента по указанному каналу (thread_id) и идентификатору запуска (run_id).'''

#     if username != USERNAME_ADMIN:
#         error_msg = f"Access denied for user '{username}'"
#         logger_api.error(error_msg)
#         return error_msg

#     model = "assistent-oa" # Пока что не знаю как и че делать с этим..

#     # Verify user and their appkey (подтверждение авторизации):
#     verification = await verify_user_appkey(username, model, appkey)
#     if verification.get("status_code") != status.HTTP_200_OK:
#         logger_api.error("User verification failed: %s", verification)
#         return verification


#     return await oa_assist_retrieve(run_id, thread_id)



# # Получение списка Асистентов:
# @app.post("/api/oa-assist-list/", status_code=status.HTTP_200_OK)
# async def in_oa_assist_list(
#     username: str = Form(...),
#     appkey: str = Header(...)
# ):

#     '''Получение списка агентов'''

#     if username != USERNAME_ADMIN:
#         error_msg = f"Access denied for user '{username}'"
#         logger_api.error(error_msg)
#         return error_msg

#     model = "assistent-oa" # Пока что не знаю как и че делать с этим..

#     # Verify user and their appkey (подтверждение авторизации):
#     verification = await verify_user_appkey(username, model, appkey)
#     if verification.get("status_code") != status.HTTP_200_OK:
#         logger_api.error("User verification failed: %s", verification)
#         return verification

#     return await oa_assist_list()



# # Удаление ассистента:
# @app.post("/api/oa-assist-del/", status_code=status.HTTP_200_OK)
# async def in_oa_assist_del(
#     username: str = Form(...),
#     appkey: str = Header(...),
#     assistant_id: str = Form(...)
# ):

#     '''Удаление Ассистента'''

#     if username != USERNAME_ADMIN:
#         error_msg = f"Access denied for user '{username}'"
#         logger_api.error(error_msg)
#         return error_msg

#     model = "assistent-oa" # Пока что не знаю как и че делать с этим..

#     # Verify user and their appkey (подтверждение авторизации):
#     verification = await verify_user_appkey(username, model, appkey)
#     if verification.get("status_code") != status.HTTP_200_OK:
#         logger_api.error("User verification failed: %s", verification)
#         return verification
    
#     return await oa_assist_del(assistant_id)




# # Удаление Thread:
# @app.post("/api/oa-thread-del/", status_code=status.HTTP_200_OK)
# async def in_oa_thread_del(
#     username: str = Form(...),
#     appkey: str = Header(...),
#     thread_id: str = Form(...)
# ):

#     '''Удаление Thread'''

#     if username != USERNAME_ADMIN:
#         error_msg = f"Access denied for user '{username}'"
#         logger_api.error(error_msg)
#         return error_msg

#     model = "assistent-oa" # Пока что не знаю как и че делать с этим..

#     # Verify user and their appkey (подтверждение авторизации):
#     verification = await verify_user_appkey(username, model, appkey)
#     if verification.get("status_code") != status.HTTP_200_OK:
#         logger_api.error("User verification failed: %s", verification)
#         return verification
    
#     return await oa_thread_del(thread_id)




# # Возврат результата Агенту:
# @app.post("/api/oa-return-result-assist/", status_code=status.HTTP_200_OK)
# async def in_oa_thread_del(
#     username: str = Form(...),
#     appkey: str = Header(...),
#     run_id: str = Form(...),
#     thread_id: str = Form(...),
#     tool_outputs: str = Form(...)
# ):

#     '''Возврат результата Агенту'''

#     if username != USERNAME_ADMIN:
#         error_msg = f"Access denied for user '{username}'"
#         logger_api.error(error_msg)
#         return error_msg

#     model = "assistent-oa" # Пока что не знаю как и че делать с этим..

#     # Verify user and their appkey (подтверждение авторизации):
#     verification = await verify_user_appkey(username, model, appkey)
#     if verification.get("status_code") != status.HTTP_200_OK:
#         logger_api.error("User verification failed: %s", verification)
#         return verification
    
#     return await oa_returning_result_assist(run_id, thread_id, tool_outputs)











# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )



# # Block frequent requests from the same IP:
# ip_request_counts = defaultdict(list)
# lock = asyncio.Lock() # "Creating" (Создание) lock.

# @app.middleware("http")
# async def rate_limit_and_log(request: Request, call_next):
#     '''Middleware для ограничения частоты запросов по IP (rate limiting).
    
#     Подсчитывает запросы от каждого IP в окне TIME_WINDOW секунд.
#     При превышении лимита REQUEST_LIMIT возвращает HTTP 429.
    
#     Args:
#         request: Входящий HTTP-запрос
#         call_next: Функция для вызова следующего обработчика
        
#     Returns:
#         Response: Ответ сервера или HTTP 429 при превышении лимита

#     Логирует запросы.
#     '''
#     ip = request.client.host
#     now = datetime.now()
#     time_window_start = now - timedelta(seconds=TIME_WINDOW)

#     # ---- request data ------------------------------------------------------
#     client_host = request.client.host
#     method      = request.method
#     url_path    = request.url.path
#     query       = request.url.query
#     try:
#         body = await request.body()
#         body = body.decode() if body else ""
#     except Exception:
#         body = "<unable to read body>"
#     # ------------------------------------------------------------------------

#     logger_api.info(f"{client_host} -> {method} {url_path}?{query} | body={body[:200]}")



#     async with lock: # "Acquiring" (Получение) lock.
#         ip_request_counts[ip] = [t for t in ip_request_counts[ip] if t > time_window_start]
#         ip_request_counts[ip].append(now)
#         request_count = len(ip_request_counts[ip])

#     if request_count > REQUEST_LIMIT:
#         logger_api.error(f"Rate limit exceeded for IP: {ip}")
#         return Response(status_code=429, content="Too Many Requests")

#     response = await call_next(request)

#     elapsed = (datetime.now() - now) * 1000
#     logger_api.info(
#         f"{client_host} <- {method} {url_path} | "
#         f"status={response.status_code} | {elapsed:.1f}ms"
#     )


#     return response
















# # --------------------------------------------------------------------
# _ip_hits: dict[str, Deque[float]] = defaultdict(deque)
# lock = asyncio.Lock()


# def _client_ip(request: Request) -> str:
#     """IP клиента с учётом прокси."""
#     xff = request.headers.get("x-forwarded-for")
#     return xff.split(",")[0].strip() if xff else request.client.host


# @app.middleware("http")
# async def rate_limit_and_log(request: Request, call_next):
#     start_ts = time.time()
#     ip = _client_ip(request)

#     # ----------- Логируем входящий запрос ---------------------------------
#     method = request.method
#     path   = request.url.path
#     query  = request.url.query

#     try:
#         body_bytes = await request.body()
#         body = body_bytes.decode(errors="replace")[:200]
#     except Exception:
#         body = "<unable to read body>"

#     logger_api.info(f'{ip} -> {method} {path}?{query} | body={body}')
#     #logger_api.info(f'ip: {ip} -> method: {method} {path}?{query} | body={body}')

#     # ----------- Rate-limit ----------------------------------------------
#     async with lock:
#         hits = _ip_hits[ip]
#         now = time.time()
#         boundary = now - TIME_WINDOW
#         # чистим старые записи
#         while hits and hits[0] < boundary:
#             hits.popleft()
#         hits.append(now)
#         if len(hits) > MAX_DEQUE_LEN:
#             hits.popleft()  # для надёжности, чтобы очередь не пухла
#         exceeded = len(hits) > REQUEST_LIMIT

#     if exceeded:
#         logger_api.warning(f"429 Too Many Requests for {ip} ({len(hits)}/{REQUEST_LIMIT})")
#         return Response(status_code=429, content="Too Many Requests")

#     # ----------- Продолжаем обработку ------------------------------------
#     try:
#         response = await call_next(request)
#     except Exception as exc:
#         logger_api.exception(f"Error while processing request from {ip}")
#         raise exc

#     elapsed_ms = (time.time() - start_ts) * 1000
#     logger_api.info(f'{ip} <- {method} {path} | {response.status_code} | {elapsed_ms:.1f}ms')
#     return response









# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # Protection from poking
# ip_request_counts = defaultdict(list)
# lock = asyncio.Lock() # "Creating" (Создание) lock.

# @app.middleware("http")
# async def rate_limit(request: Request, call_next):
#     ip = request.client.host
#     now = datetime.now()
#     time_window_start = now - timedelta(seconds=TIME_WINDOW)

#     async with lock: # "Acquiring" (Получение) lock.
#         ip_request_counts[ip] = [t for t in ip_request_counts[ip] if t > time_window_start]
#         ip_request_counts[ip].append(now)
#         request_count = len(ip_request_counts[ip])

#     if request_count > REQUEST_LIMIT:
#         logger_api.critical(f"Rate limit exceeded for IP: {ip}")
#         return Response(status_code=429, content="Too Many Requests")

#     response = await call_next(request)
#     return response