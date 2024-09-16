from pathlib import Path
from openai import AsyncOpenAI, RateLimitError, OpenAIError
import aiofiles

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

    print()
    print(response.text)
    print()

    speech_file_path = Path('./audio/speech.mp3')
    
    async with aiofiles.open(speech_file_path, 'wb') as audio_file:
        await audio_file.write(response.content)

        return speech_file_path


        # # Statistic
        # used_tokens = length_of_audio
        # model_version = model # just only whisper-1
        
        # # Calculation of money spent on minutes + sec
        # expenses = await calculation(username, model_version, used_tokens, input_data="audio")

        # return {"response":transcript, "expenses": expenses, "minutes": used_tokens / 60}











