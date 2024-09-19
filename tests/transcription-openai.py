import requests

url = "http://137.184.87.156:8000/api/transcription-openai/"

data = {
        "username": "Shliamb5", # !
        "prompt": "переведи в текст",
        "language": "ru", # input language in ISO-639-1, will improve accuracy and latency - ru or en
        "model": "whisper-1", # whisper-1
        "response_format": "text", # json, text, srt, verbose_json, or vtt
        # timestamp_granularities=["word"],
        # timestamp_granularities=["segment"]
}

headers = {
    'appkey': 'a36c0e6c-6123-42e9-bcda-1c16e0c7e201',
}

with open('./audio/in_audio_2.ogg', 'rb') as f:
    
    file = {
        'audio': ('in_audio_2.ogg', f)
    }

    response = requests.post(url, headers=headers, data=data, files=file)

# Проверка статуса ответа и вывод результата
if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)