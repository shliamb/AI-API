from openai import AsyncOpenAI, RateLimitError, OpenAIError
from keys import API_KEY_OPENAI
import aiofiles
from general_functions import calculation, read_audio_file

client = AsyncOpenAI(api_key=API_KEY_OPENAI)

async def translation_openai(description, audio_path):

    username = description.get("username")
    prompt = description.get("prompt")
    language = description.get("language") # input language in ISO-639-1, will improve accuracy and latency - ru or en
    model = description.get("model", "whisper-1") # whisper-1 only now
    response_format = description.get("response_format", "text") # json, text, srt, verbose_json, or vtt

    with open(audio_path, "rb") as file:

        transcript = await client.audio.translations.create(
            model = model,
            prompt = prompt,
            response_format = response_format,
            file = file,
        )

        length_of_audio = await read_audio_file(audio_path)   # mp3 (ID3v1 и ID3v2), flac, ogg Vorbis, acc (and M4A), wav, wma (limited support), aiff

        # Statistic
        min = length_of_audio / 60 # from minutes
        model_version = model # just only whisper-1
        
        # Calculation of money spent on minutes + sec
        expenses = await calculation(username, model_version, min, input_data="audio")

        return {"response":transcript, "expenses": expenses, "minutes": min}










'''



Suport files Mutagen:

  - MP3 (ID3v1 и ID3v2)
  - FLAC
  - Ogg Vorbis
  - AAC (включая M4A)
  - WAV
  - WMA (ограниченная поддержка)
  - AIFF

  


'''