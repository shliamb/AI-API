import requests
from config import HOST
import base64

url = f"http://{HOST}/api/openai-text-to-voice/"

data = {
        "access_id": "08a898f3-e6dd-49c2-93a7-fff0abc7ad31",
        "user_content": "А ну-у-у-у-ка! Подика сюда, мальчик.)",
        "voice": "nova", # alloy, echo, fable, onyx, nova, and shimmer
        "model": "tts-1", # tts-1 or tts-1-hd
        "response_format": "wav", # mp3, opus, aac, flac, wav, and pcm
        "speed": 1.0, # 0.25 to 4.0
}

headers = {
    "some_key": "d98f74a7-81de-4afd-b06d-94cb6cb821fc",
}

response = requests.post(url, headers=headers, data=data)

format_audio = data["response_format"]

if response.status_code == 200:
    # Получаем JSON-ответ
    json_response = response.json()
    b64_json = json_response.get("b64_json")

    if b64_json:
        # Декодируем строку Base64 обратно в бинарные данные
        audio_data = base64.b64decode(b64_json)

        # Сохраняем аудиофайл локально
        with open(f"./audio/output_audio.{format_audio}", "wb") as audio_file:
            audio_file.write(audio_data)

        print(f"The audio file is saved as output_audio.{format_audio}")

    elif isinstance(response, str):
        print(f"Error: {response}")

else:
    if isinstance(response, str):
        print(f"Error: {response}")
