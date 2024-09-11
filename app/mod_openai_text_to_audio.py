from pathlib import Path
import openai









async def speech_to_audio_openai(description):

    username = description.get("username")
    user_content = description.get("user_content")
    voice = description.get("voice", "alloy") # alloy, echo, fable, onyx, nova, and shimmer
    model = description.get("model", "tts-1") # tts-1 or tts-1-hd
    response_format = description.get("response_format", "mp3") # mp3, opus, aac, flac, wav, and pcm
    speed = description.get("speed", "1") # 0.25 to 4.0. default - 1.0




    speech_file_path = Path('./audio/speech.mp3') # speech_file_path = Path(__file__).parent / "speech.mp3" speech_file_path = Path(__file__).parent / 'audio' / 'speech.mp3'
    response = openai.audio.speech.create(
        model = model,
        voice = voice,
        response_format = response_format,
        speed = speed,
        input = user_content
    )

    #response.stream_to_file(speech_file_path)
    print(speech_file_path)
    return response.with_streaming_response.method(speech_file_path)












