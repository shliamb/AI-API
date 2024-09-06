import google.generativeai as genai
from keys import api_key_gemini, is_admin


genai.configure(api_key=api_key_gemini)







async def mod_gemini(username, user_input):
    model = genai.GenerativeModel(model_name=user_input.model, tools=user_input.tools or None) # gemini-1.5-flash-001  "gemini-1.5-flash"
    # organ = PIL.Image.open(media / "organ.jpg")
    response = model.generate_content(user_input.user_content)
    return {"response": response.text}


# # Set the `response_mime_type` to output JSON
# generation_config={"response_mime_type": "application/json"})=




"""
1m token


модель: gemini-1.5-flash
вход: Аудио, изображения, видео и текст
выход: Текст
для: Быстрая и универсальная производительность при выполнении широкого спектра задач. 
price: 0,5625 $ 1m token


модель: gemini-1.5-pro
вход: Аудио, изображения, видео и текст
выход: Текст
для: Сложные задачи рассуждения, такие как генерация кода и текста, редактирование текста, решение проблем, извлечение и генерация данных.
price: 46,875 $


модель: gemini-1.0-pro - что то не то с названием модели
вход: Текст
выход: Текст
для: Задачи на естественном языке, многоходовой текстовый и кодовый чат, а также генерация кода 
price: 2 $


модель: text-embedding-004 - что то не то с названием модели
вход: Текст
выход: Встраивание текста
для: Измерение связанности текстовых строк
price: 0 $


модель: aqa
вход: Текст
выход: Текст
для: Предоставление обоснованных ответов на вопросы
price: 



2023 год

Чтобы указать последнюю версию, используйте следующий шаблон: <model>-<generation>-<variation>-latest . Например, gemini-1.0-pro-latest 

"""