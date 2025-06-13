import requests
from config import HOST

url = f"http://{HOST}/api/openai-voice-to-text/"

data = {
        "access_id": "08a898f3-e6dd-49c2-93a7-fff0abc7ad31",
        "prompt": "переведи в текст",
        "language": "ru", # input language in ISO-639-1, will improve accuracy and latency - ru or en
        "model": "whisper-1", # whisper-1
        "response_format": "text", # json, text, srt, verbose_json, or vtt
        # timestamp_granularities=["word"],
        # timestamp_granularities=["segment"]
}

headers = {
    "some_key": "d98f74a7-81de-4afd-b06d-94cb6cb821fc",
}

with open('./audio/in_audio_2.ogg', 'rb') as f:
    
    file = {
        'file': ('in_audio_2.ogg', f)
    }

    response = requests.post(url, headers=headers, data=data, files=file)

# Проверка статуса ответа и вывод результата
if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)