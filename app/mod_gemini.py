import google.generativeai as genai
from keys import api_key_gemini, is_admin


genai.configure(api_key=api_key_gemini)







async def mod_gemini(user_input):
    model = genai.GenerativeModel(user_input.model) # gemini-1.5-flash-001  "gemini-1.5-flash"
    response = model.generate_content(user_input.user_content)
    print(response.text)
    return {"response": response.text}










"""
модель gemini-1.5-flash
вход Аудио, изображения, видео и текст
выход Текст
для Быстрая и универсальная производительность при выполнении широкого спектра задач. 


модель gemini-1.5-pro
вход Аудио, изображения, видео и текст
выход Текст
для Сложные задачи рассуждения, такие как генерация кода и текста, редактирование текста, решение проблем, извлечение и генерация данных.


модель gemini-1.0-pro
вход Текст
выход Текст
для Задачи на естественном языке, многоходовой текстовый и кодовый чат, а также генерация кода 


модель text-embedding-004
вход Текст
выход Встраивание текста
для Измерение связанности текстовых строк


модель aqa
вход Текст
выход Текст
для Предоставление обоснованных ответов на вопросы


2023 год

Чтобы указать последнюю версию, используйте следующий шаблон: <model>-<generation>-<variation>-latest . Например, gemini-1.0-pro-latest 

"""