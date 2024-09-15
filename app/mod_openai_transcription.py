from pathlib import Path
from openai import AsyncOpenAI, RateLimitError, OpenAIError
import aiofiles

# from io import BytesIO
import io

from keys import api_key_openai


client = AsyncOpenAI(api_key=api_key_openai)


async def transcription_openai(description, audio_path):

    username = description.get("username")
    prompt = description.get("prompt")
    language = description.get("language") # input language in ISO-639-1, will improve accuracy and latency - ru or en
    model = description.get("model", "whisper-1") # whisper-1 only now
    response_format = description.get("response_format", "text") # json, text, srt, verbose_json, or vtt

    async with aiofiles.open(audio_path, "rb") as file:
        content = await file.read()  # Читаем содержимое файла

    # Оборачиваем байты в BytesIO
    file_like_object = io.BytesIO(content)

    # content = open(audio_path, "rb")

    transcript = await client.audio.transcriptions.create(
        model = model,
        prompt = prompt,
        language = language,
        response_format = response_format,
        # timestamp_granularities=["word"],
        # timestamp_granularities=["segment"]
        file = file_like_object,
    )

    return transcript



