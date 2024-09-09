
#### CONFIG ####

limit_trying = 5
timeout_after_error_username = 5 # sec.
waiting_time = 15 # min/
time_correction = +3 # Moscow
money_to_start = 1 # 1$ to start work
my_app_key = "appkey" # Key to API Key
min_pay = 1 # Minimum pay
ai_default_model = "gpt-4o-mini-2024-07-18"



# Prices per 1M tokens:
# Важно, нужно размещать выше дорогие однокоренные модели, что бы не хитрили
price = {
    # OpenAI:
    'chatgpt-4o-latest': 40,
    'gpt-4o': 40,
    'gpt-4o-2024-05-13': 40,
    'gpt-4o-2024-08-06': 25,
    'gpt-4o-mini': 1.5, # no vision
    'gpt-4o-mini-2024-07-18': 1.5, # no vision
    'gpt-4-turbo-2024-04-09': 80,

    # Images:
    'dall-e-3-1024': 0.08,
    'dall-e-3-1792': 0.16,

    'dall-e-3-hd-1024': 0.16,
    'dall-e-3-hd-1792': 0.24,

    'dall-e-2-1024': 0.04,
    'dall-e-2-512': 0.036,
    'dall-e-2-256': 0.032,

    # Google Gemini:
    'gemini-1.5-pro-latest': 93.75,
    'gemini-1.5-flash-latest': 1.125,
    'gemini-1.0-pro-latest': 4,
    # 'text-embedding-004': 0, # Free  хз пока что как ее пользовать
    # 'aqa': 0,
    }



# Instruction API OpenAI: https://platform.openai.com/docs/api-reference/chat/create
# Price OpenAI: https://openai.com/api/pricing/






"""

5Sep2024 OpenAI 1m tokens:

Model                         Input $              Output $           Total $

chatgpt-4o-latest                 5                   10                 20
gpt-4o                            5                   15                 20
gpt-4o-2024-08-06                 2.5                 10                 12.5           
gpt-4o-2024-05-13                 5                   15                 20
gpt-4o-mini                       0.15                0.6                0.75
gpt-4o-mini-2024-07-18            0.15                0.6                0.75
gpt-4-turbo-2024-04-09            10                  30                 40




Model                   Quality                       Resolution                      Price     

dall-e-3                Standart                      1024×1024                       0.04$ / image
dall-e-3                Standart                      1024×1792, 1792×1024            0.080$ / image     

dall-e-3                HD                            1024×1024                       0.080$ / image
dall-e-3                HD                            1024×1792, 1792×1024            0.120$ / image 

dall-e-2                                              1024×1024                       0.020$ / image
dall-e-2                                              512×512                         0.018$ / image 
dall-e-2                                              256×256                         0.016$ / image 



dall-e-3-1024       0.04
dall-e-3-1792       0.08

dall-e-3-hd-1024    0.08
dall-e-3-hd-1792    0.12

dall-e-2-1024       0.02
dall-e-2-512        0.018
dall-e-2-256        0.016


'dall-e-3-1024': 0.04,
'dall-e-3-1792': 0.08,

'dall-e-3-hd-1024': 0.08,
'dall-e-3-hd-1792': 0.12,

'dall-e-2-1024': 0.02,
'dall-e-2-512': 0.018,
'dall-e-2-256': 0.016,




Model         Usage $

Whisper       0.006/minute (rounded to the nearest second)
TTS           15/1M characters
TTS HD        30/1M characters


"""









"""
6Sep2024 Gemini 1m tokens


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









"""
Видео или аудио файлы
Аудио и видео конвертируются в токены по следующим фиксированным ставкам:

Видео: 263 токена в секунду
Аудио: 32 токена в секунду

"""