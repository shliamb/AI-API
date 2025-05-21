#### CONFIG ####
LIMIT_TRY = 5
TIME_OUT_ERR_USERNAME = 5 # sec.
WAITING_TIME = 15 # min/
TIME_CORRECTION = +3 # Moscow
MONEY_TO_START = 0.3 # 1$ to start work
MY_APP_KEY = "appkey" # Key to API Key
MIN_PAY = 1 # Minimum pay

# Folders:
UPLOADS = "./uploads/"
AUDIO_FOLDER = "./audio/"
# AI Defoult:
DEF_MOD_GOOGLE = "gemini-2.0-flash-exp"
DEF_MOD_OPENAI = "gpt-4o-mini-2024-07-18"
DEF_MOD_GROK = "grok-2-vision-latest"
DEF_MOD_CLAUDE = "claude-3-haiku-20240307"
DEF_CLAUDE_VERSION = "2023-06-01" # Специфичная для антропик вешь..

# api.py
REQUEST_LIMIT = 10 # Максимальное количество запросов с одного IP-адреса в течение TIME_WINDOW секунд.
TIME_WINDOW = 60 # Интервал времени в секундах, в течение которого действует ограничение.



# Prices per 1M tokens:
# Важно, нужно размещать выше дорогие однокоренные модели, что бы не хитрили
PRICE = {
    # OpenAI to 1M tokes:

    # New:


    'gpt-4.1': 12, # 1 million Contex gpt-4.1-2025-04-14
    'gpt-4.1-mini': 2.4, # gpt-4.1-mini-2025-04-14
    'gpt-4.1-nano': 0.6, # gpt-4.1-nano-2025-04-14

    'gpt-4.5-preview': 270, # gpt-4.5-preview-2025-02-27
    'o1-pro': 900, # o1-pro-2025-03-19
    'o1': 90, # o1-2024-12-17
    'o1-preview': 90,

    'o3': 60, # o3-2025-04-16 

    'o4-mini': 6.6, # o4-mini-2025-04-16 
    'o3-mini': 6.6, # 
    'o1-mini': 6.6,
    # 'gpt-4o-mini-search-preview': 0.9,
    # 'gpt-4o-search-preview': 15,
    # 'computer-use-preview': 18,
    'chatgpt-4o-latest': 24,
    'gpt-4o': 24,
    'gpt-4o-2024-05-13': 24,
    'gpt-4o-2024-08-06': 15,
    'gpt-4o-mini': 1.8, # no vision
    'gpt-4o-mini-2024-07-18': 1.8, # no vision
    'gpt-4-turbo-2024-04-09': 48,

    # Images to one img:
    'dall-e-3-1024': 0.048,
    'dall-e-3-1792': 0.096,

    'dall-e-3-hd-1024': 0.096,
    'dall-e-3-hd-1792': 0.144,

    'dall-e-2-1024': 0.024,
    'dall-e-2-512': 0.0216,
    'dall-e-2-256': 0.0192,

    # Audio to 1M characters:
    'tts-1': 18, # / 1M characters
    'tts-1-hd': 36, # / 1M characters
    'whisper-1': 0.0072, # minute (rounded to the nearest second)

    # Elon Musk Grok to 1M tokens:
    'grok-3-latest': 21.6, # Contex 131072, 
    'grok-3-fast-latest': 36, # Contex 131072, 
    'grok-3-mini-latest': 0.96, # Contex 131072,
    'grok-3-mini-fast-latest': 5.52, # Contex 131072,

    'grok-vision-beta': 24, # Text, Image = 6, Contex 8192, 
    'grok-2-vision-latest': 14.4, # Text, Image = 2.4, Contex 32768, 
    'grok-2-latest': 14.4, # Only Text, Contex 131072, 
    'grok-beta': 24, # Only Text, Contex 131072, 

    # Google Gemini to 1M tokens:
    'gemini-2.5-pro-preview-03-25': 21,# Maximum input tokens 1,048,576
    'gemini-2.0-flash-exp': 0.9, # 15,
    'gemini-2.0-flash-lite-001': 0.45,
    'gemini-1.5-pro-latest': 3.75, # 15, 
    'gemini-1.5-flash-latest': 0.225, # 0.8,
    'gemini-1.5-flash-8b': 0.5,

    # Antropic Claude to 1M tokens:  Context window - 200k, 
    # New:
    'claude-3-7-sonnet-latest': 21.6, # 200K context window Most intelligent model, with visible step‑by‑step reasoning claude-3-7-sonnet-20250219
    'claude-3-5-sonnet-latest': 21.6, # output 8192 tokens
    'claude-3-5-haiku-latest': 5.76, # no vision and output 8192 tokens
    'claude-3-opus-latest': 108, # 4096 tokens
    # Old:
    'claude-3-sonnet-20240229': 21.6, # 4096 tokens
    'claude-3-haiku-20240307': 1.8, # 200K context window

    }



# Instruction API OpenAI: https://platform.openai.com/docs/api-reference/chat/create
# Price OpenAI: https://openai.com/api/pricing/






"""



6Nov2024 OpenAI 1m tokens:

Model                         Input $              Output $           Total $

Old:
Claude 3 Haiku                 0.25                   1.25                 1.5
Claude 3 Sonnet                3                      15                   18 

New:
Claude 3.5 Haiku               1                      5                    6
Claude 3.5 Sonnet              3                      15                   18           
Claude 3 Opus                  15                     75                   90






5Sep2024 OpenAI 1m tokens:

Model                         Input $              Output $           Total $

chatgpt-4o-latest                 5                   10                 20
gpt-4o                            5                   15                 20
gpt-4o-2024-08-06                 2.5                 10                 12.5           
gpt-4o-2024-05-13                 5                   15                 20
gpt-4o-mini                       0.15                0.6                0.75
gpt-4o-mini-2024-07-18            0.15                0.6                0.75
gpt-4-turbo-2024-04-09            10                  30                 40
o1-preview                        15                  60                 75
o1-preview-2024-09-12             15                  60                 75
o1-mini                           3                   12                 15
o1-mini-2024-09-12                3                   12                 15




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