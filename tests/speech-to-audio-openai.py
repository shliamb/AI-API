import requests
import base64

url = "http://137.184.87.156:8000/api/speech-to-audio-openai/"

data = {
        "username": "Shliamb10",
        "user_content": "Вот зараза..",
        "voice": "nova", # alloy, echo, fable, onyx, nova, and shimmer
        "model": "tts-1", # tts-1 or tts-1-hd
        "response_format": "mp3", # mp3, opus, aac, flac, wav, and pcm
        "speed": 1.0, # 0.25 to 4.0
}

headers = {
    'appkey': '72d3d8e8-74c4-4ff6-9033-91e8670b3708',
}

response = requests.post(url, headers=headers, data=data)



if response.status_code == 200:
    # Получаем JSON-ответ
    json_response = response.json()
    b64_json = json_response.get("b64_json")

    if b64_json:
        # Декодируем строку Base64 обратно в бинарные данные
        audio_data = base64.b64decode(b64_json)

        # Сохраняем аудиофайл локально
        with open("./audio/output_audio.mp3", "wb") as audio_file:
            audio_file.write(audio_data)

        print("Аудиофайл сохранен как output_audio.mp3")
else:
    print(f"Ошибка: {response.status_code} - {response.text}")
