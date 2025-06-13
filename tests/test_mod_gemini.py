import requests
from config import HOST

path_file = None

#path_file = "./uploads/image45.png"


url = f"http://{HOST}/api/gemini/"

data = {
        "access_id": "08a898f3-e6dd-49c2-93a7-fff0abc7ad31",
        "user_content": "Привет как твои дела?", # !
        #"system_content": "Ответь по русски.",
        #"model": "gemini-2.0-flash-exp",
        #'assist_content': '[{"user": "How do I charge my battery?"}, {"assistant": "You should use the provided charging cable."}, {"user": "But it doesn\'t seem to charge."}, {"assistant": "Try another charge.."}]',
        # ?? 'response_format':'[generationConfig: {responseMimeType: "application/json",responseSchema: {type: SchemaType.ARRAY,items: {type: SchemaType.OBJECT,properties: {recipe_name: {type: SchemaType.STRING,},},},},}});]'
}

headers = {
    "some_key": "d98f74a7-81de-4afd-b06d-94cb6cb821fc",
}


if path_file:
    with open(path_file, 'rb') as f:
        file = {'file': ('image45.png', f)}
        response = requests.post(url, headers=headers, data=data, files=file)
else:
    response = requests.post(url, headers=headers, data=data)



if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)

print(response)