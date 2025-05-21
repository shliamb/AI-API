# from pathlib import Path
from openai import AsyncOpenAI, RateLimitError, OpenAIError
import aiofiles
import tiktoken
from general_functions import calculation, random_name_2X
from config import AUDIO_FOLDER

from keys import API_KEY_OPENAI


client = AsyncOpenAI(api_key=API_KEY_OPENAI)


async def speech_to_audio_openai(description):

    username = description.get("username")
    user_content = description.get("user_content")
    voice = description.get("voice", "alloy") # alloy, echo, fable, onyx, nova, and shimmer
    model = description.get("model", "tts-1") # tts-1 or tts-1-hd
    response_format = description.get("response_format", "mp3") # mp3, opus, aac, flac, wav, and pcm
    speed = description.get("speed", "1") # 0.25 to 4.0. default - 1.0

    response = await client.audio.speech.create(
        model = model,
        voice = voice,
        response_format = response_format,
        speed = speed,
        input = user_content
    )

    name = random_name_2X()
    speech_file_path = f"{AUDIO_FOLDER}{name}-audio.{response_format}" # speech_file_path = Path('./audio/speech.mp3')
    
    async with aiofiles.open(speech_file_path, 'wb') as audio_file:
        await audio_file.write(response.content)

        # Statistic *** Ебанный костыль, пока что не знаю как подругому сделать ****   Available encodings: ['gpt2', 'r50k_base', 'p50k_base', 'p50k_edit', 'cl100k_base', 'o200k_base']
        enc = tiktoken.get_encoding("gpt2")
        tokens = enc.encode(user_content)
        used_tokens = len(tokens)
        model_version = model # just only tts-1

        # Calculation of money spent on tokens
        expenses = await calculation(username, model_version, used_tokens, input_data="text")

        # print(f"response: {speech_file_path}, expenses: {expenses}, minutes: {used_tokens}")
        return speech_file_path









        # Получить список всех зарегистрированных кодировок  Available encodings: ['gpt2', 'r50k_base', 'p50k_base', 'p50k_edit', 'cl100k_base', 'o200k_base']
        # available_encodings = tiktoken.list_encoding_names()
        # print("Available encodings:", available_encodings)
