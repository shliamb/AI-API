from pathlib import Path
from openai import AsyncOpenAI, RateLimitError, OpenAIError
import aiofiles

from keys import api_key_openai


client = AsyncOpenAI(api_key=api_key_openai)



async def read_file_async(audio_path):
    async with aiofiles.open(audio_path, 'rb') as file:
        content = await file.read()
    return content




async def transcription_openai(description, audio_path):

    username = description.get("username")
    prompt = description.get("prompt")
    language = description.get("language") # input language in ISO-639-1, will improve accuracy and latency - ru or en
    model = description.get("model", "whisper-1") # whisper-1 only now
    response_format = description.get("response_format", "text") # json, text, srt, verbose_json, or vtt

    #async with aiofiles.open(audio_path, "rb") as file:
        # content = await file.read()  # Читаем содержимое файла
    #content = open(audio_path, "rb")
    content = await read_file_async(audio_path)

    transcript = await client.audio.transcriptions.create(
        model = model,
        prompt = prompt,
        language = language,
        response_format = response_format,
        # timestamp_granularities=["word"],
        # timestamp_granularities=["segment"]
        file = content
    )

    return transcript



