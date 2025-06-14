from config import AUDIO_FOLDER, LOG_CONFIG_AI, TIMEOUT_SERVER_AI
import logging
logging.basicConfig(**LOG_CONFIG_AI)
from openai import AsyncOpenAI, OpenAIError
import aiofiles
import tiktoken
import asyncio
from general_functions import DictObj, random_name
from store_token_cost import calculate_token_cost
from keys import API_KEY_OPENAI


client = AsyncOpenAI(api_key=API_KEY_OPENAI)


async def openai_text_to_voice(description: dict) -> str:
    '''Модуль перевода текста в голос от OpenAI'''

    dict_des = DictObj(description)
    access_id = dict_des.access_id
    user_content = dict_des.user_content
    voice = dict_des.voice or "nova"                        # alloy, echo, fable, onyx, nova, and shimmer
    model = dict_des.model or "tts-1"                       # tts-1 or tts-1-hd
    response_format = dict_des.response_format or "opus"     # mp3, opus, aac, flac, wav, and pcm
    speed = dict_des.speed                                  # 0.25 to 4.0. default - 1.0

    logging.info(f"{access_id} -> 'main API OpenAI text to voice'")
    print(f"INFO: {access_id} -> 'main API OpenAI text to voice'")

    try:
        print("1")
        print(model, voice, response_format, speed, user_content, TIMEOUT_SERVER_AI)


        # Работает
        response = await client.audio.speech.create(
            model = "gpt-4o-mini-tts", #model, # "gpt-4o-mini-tts"
            voice = voice, 
            response_format = response_format,
            #speed = speed,
            input = user_content
        )


        # file_path = f"{AUDIO_FOLDER}{random_name()}-audio.{response_format}"

        # async with client.audio.speech.with_streaming_response.create(
        # model="gpt-4o-mini-tts",
        # voice="alloy",
        # input="The quick brown fox jumped over the lazy dog."
        # ) as response:
        #     await response.stream_to_file(file_path)
        #     print("69")
        #     print(file_path)
        #     return file_path

        # response = await client.audio.speech.acreate(
        #     model="gpt-4o-mini-tts",
        #     voice="alloy",
        #     input=text
        # )
        # output_path.write_bytes(response.content)

        # response = await asyncio.wait_for(client.audio.speech.create(
        #     model = "gpt-4o-mini-tts", #model,
        #     voice = "alloy", #voice,
        #     response_format = response_format,
        #     speed = speed,
        #     input = user_content
        # ), timeout=TIMEOUT_SERVER_AI)


        print(f"INFO: 'main API OpenAI text to voice' -> get response")
        logging.info(f"'main API OpenAI text to voice' -> get response")

        # if isinstance(response, str):
        #     print("2")
        #     logging.error("Error: OpenAi Server text to voice")
        #     return response

    except asyncio.TimeoutError as e:
        print("3")
        print(f"OpenAI Server timeout: {str(e)}")
        logging.error(f"OpenAI Server timeout: {str(e)}", exc_info=True)
        return response if isinstance(response, str) else None

    except OpenAIError as e:  # Используем прямое имя модуля
        print("4")
        print(f"OpenAI API error: {str(e)}")
        logging.error(f"OpenAI API error: {str(e)}", exc_info=True)
        return str(e)  # Всегда возвращаем строку с описанием ошибки

    except Exception as e:
        print("5")
        print(f"Unexpected error in text-to-voice: {str(e)}")
        logging.critical(f"Unexpected error in text-to-voice: {str(e)}", exc_info=True)
        return f"Internal error: {str(e)}" if str(e) else None
        



    # TOKENS:
    try:
        print("6")
        file_path = f"{AUDIO_FOLDER}{random_name()}-audio.{response_format}" # speech_file_path = Path('./audio/speech.mp3')
        
        async with aiofiles.open(file_path, 'wb') as audio_file:
            await audio_file.write(response.content)
            # Statistic *** Ебанный костыль, пока что не знаю как подругому сделать ****   Available encodings: ['gpt2', 'r50k_base', 'p50k_base', 'p50k_edit', 'cl100k_base', 'o200k_base']
            enc = tiktoken.get_encoding("gpt2")
            tokens = enc.encode(user_content)
            used_tokens = len(tokens)
            model_version = model # just only tts-1


            print(access_id, model_version, used_tokens)
            if not await calculate_token_cost(access_id, model_version, used_tokens, input_data="text"):
                logging.error("Error: Failed to calculate tokens OpenAI main text to voice")
                return "Error: Failed to calculate tokens OpenAI main text to voice"

            print(file_path)
            return file_path
        
    except:
        logging.error(f"Error: Failed to calculate tokens OpenAI main text to voice: {e}")
        return f"Error: Failed to calculate tokens OpenAI main text to voice: {e}"







# Получить список всех зарегистрированных кодировок  Available encodings: ['gpt2', 'r50k_base', 'p50k_base', 'p50k_edit', 'cl100k_base', 'o200k_base']
# available_encodings = tiktoken.list_encoding_names()
# print("Available encodings:", available_encodings)
