from config import TIME_CORRECTION
from datetime import datetime, timezone, timedelta
import random
import string
import os
import re
import base64
import aiofiles
import asyncio
from mutagen import File
from io import BytesIO
from setup_config_logger import setup_logger
logger_bot = setup_logger('bot', '/log/bot.log')




# Для удобтва получения из dict:
class DictObj:
    def __init__(self, d):
        for key, value in d.items():
            setattr(self, key, value)


# GET DAY AND TIME
async def day_utcnow():
    utc_zone = timezone.utc
    a = datetime.now(timezone.utc).replace(tzinfo=utc_zone)
    a = a + timedelta(hours=TIME_CORRECTION)
    day_str = a.strftime("%Y-%m-%d %H:%M:%S")
    day = datetime.strptime(day_str, '%Y-%m-%d %H:%M:%S')
    #logger_bot.info("info: Getting the day and time from the server")
    return day or None

# UNFORMAT TIME
async def unformat_date(date):
    day_now = str(date.strftime("%Y-%m-%d"))
    time_now = float(date.strftime("%H.%M"))
    return day_now, time_now


# Remove File OS
# async def remove_file_os(file_path):
#     if os.path.exists(file_path):
#         os.remove(file_path)
#         #print(f"The {file_path} file was successfully deleted.")
#         logger_bot.info(f"The {file_path} file was successfully deleted.")
#         return True
#     else:
#         #print(f"The {file_path} file does not exist.")
#         logger_bot.error(f"The {file_path} file does not exist.")
#         return False

# Remove File OS Async
async def remove_file_os(file_path):
    loop = asyncio.get_running_loop()
    
    if await loop.run_in_executor(None, os.path.exists, file_path):
        await loop.run_in_executor(None, os.remove, file_path)
        logger_bot.info(f"The {file_path} file was successfully deleted.")
        return True
    else:
        logger_bot.error(f"The {file_path} file does not exist.")
        return False
    

# Cleaner model AI
async def cleaner_model(name_model):
    pattern = r"(dall-e-\d)"
    match = re.search(pattern, name_model)
    if match:
        match = match.group(1)
    return match



# Encode the image
async def encode_file(file_path):
  async with aiofiles.open(file_path, "rb") as file:
    content = await file.read()
    return base64.b64encode(content).decode('utf-8')
  

# Async save file
async def write_file(file, file_path):
    async with aiofiles.open(file_path, "wb") as buffer:
        while content := await file.read(1024):  # Читаем файл порциями по 1024 байта
            await buffer.write(content)
            return


# Async calculating the length of an audio file:
async def read_audio_file(file_path: str) -> float: # mp3 (ID3v1 и ID3v2), flac, ogg Vorbis, acc (and M4A), wav, wma (limited support), aiff
    async with aiofiles.open(file_path, 'rb') as f:
        content = await f.read()
        audio_file = BytesIO(content)
        
        # Загружаем аудиофайл с помощью mutagen
        audio = File(audio_file)
        
        if audio is None or audio.info is None:
            #print("The audio file could not be uploaded.")
            logger_bot.error("The audio file could not be uploaded.")
        else:
            # print(audio.pprint())
            duration = audio.info.length  # Получаем длину в секундах
            if duration:
                length_sound = float(f"{duration:.2f}")
                return length_sound



# Random name to file:
def random_name() -> str:
    return f"{random.randint(101, 190)}-{random.choice(string.ascii_letters)}-{random.randint(101, 190)}"
