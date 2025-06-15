import logging

#### CONFIG ####


# TELEGRAMM and DB
HOST = "app_postgres"  # app_postgres or localhost
TIMEOUT_SERVER_AI = 300 # 3 минуты ожидания от сервера ИИ
LOG_CONFIG_DB = {
    'format': '%(levelname)s - %(asctime)s - %(name)s - %(message)s',
    'level': logging.INFO,
    'filename': './log/db.log'
}
LOG_CONFIG_BOT = {
    'format': '%(levelname)s - %(asctime)s - %(name)s - %(message)s',
    'level': logging.INFO, 
    'filename': './log/bot.log', 
    'filemode': 'a'
}
LOG_CONFIG_API = {
    'format': '%(levelname)s - %(asctime)s - %(name)s - %(message)s',
    'level': logging.INFO,
    'filename': './log/api.log'
}
LOG_CONFIG_AI = {
    'format': '%(levelname)s - %(asctime)s - %(name)s - %(message)s',
    'level': logging.INFO,
    'filename': './log/ai.log'
}
NOTIFICATION = True
COUNTS_QUANTITY = 3 # MAX Коллисчество подключений - аккаунтов телеграмм пользователю
MONEY_TO_START = 0.3 # 1$ to start work
ALLOWED_HEADER_NAMES = {"appkey", "some_key", "bad_key"}  # возможные варианты названий
GUEST_APP_KEY = "appkey"
SUPER_HEADER_NAMES = "bad_key"
MIN_PAY = 1 # Minimum pay
TIME_CORRECTION = +3 # Moscow


# FASTAPI
REQUEST_LIMIT = 10 # Максимальное количество запросов с одного IP-адреса в течение TIME_WINDOW секунд.
TIME_WINDOW = 60 # Интервал времени в секундах, в течение которого действует ограничение.
#USERNAME_ADMIN = "Alex7"



# Folders:
LOGS_FOLDER = "./log/"
UPLOADS = "./uploads/"
AUDIO_FOLDER = "./audio/"
PATH_JSON_USERS = "./json/"
DOWNLOAD = "./download/"
BACKUP_DB = "./backup_db/"

# AI Default:
DEF_MOD_GOOGLE = "gemini-1.5-flash-latest"
DEF_MOD_OPENAI = "gpt-4o-mini-2024-07-18"
DEF_MOD_GROK = "grok-2-vision-latest"
DEF_MOD_CLAUDE = "claude-3-haiku-20240307"
DEF_CLAUDE_VERSION = "2023-06-01" # Специфичная для антропик вешь..





# Prices per 1M tokens:
# Важно, нужно размещать выше дорогие однокоренные модели, что бы не хитрили
PRICE = {
    # OpenAI to 1M tokes:

    # New:

    'assistent-oa': 0.1, # Пока что хз че как


    'gpt-4.1': 12, # 1 million Contex gpt-4.1-2025-04-14
    'gpt-4.1-mini': 2.4, # gpt-4.1-mini-2025-04-14
    'gpt-4.1-nano': 0.6, # gpt-4.1-nano-2025-04-14

    'gpt-4.5-preview': 270, # gpt-4.5-preview-2025-02-27
    'o1-pro': 900, # o1-pro-2025-03-19
    'o1': 90, # o1-2024-12-17
    'o1-preview': 90,

    'o3-pro': 120, # o3-pro-2025-06-10   !!!!
    'o3': 12, # o3-2025-04-16

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
    'gpt-4o-mini-tts': 15.12, # / 1M characters
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
    'gemini-2.5-pro-preview-05-06': 13.5,# Maximum input tokens 1,048,576
    'gemini-2.5-flash-preview-04-17': 0.9, # $3.50  - Text output (thinking- response and reasoning)
    'gemini-2.0-flash-exp': 0.9, # 15,
    'gemini-2.0-flash-lite-001': 0.45,
    'gemini-1.5-pro-latest': 3.75, # 15, 
    'gemini-1.5-flash-latest': 0.225, # 0.8,
    'gemini-1.5-flash-8b': 0.5,

    # Antropic Claude to 1M tokens:  Context window - 200k, 
    # New:
    'claude-opus-4-20250514': 21.6, # claude-opus-4-20250514
    'claude-sonnet-4-20250514': 21.6, # claude-sonnet-4-20250514

    'claude-3-7-sonnet-latest': 21.6, # 200K context window Most intelligent model, with visible step‑by‑step reasoning claude-3-7-sonnet-20250219
    'claude-3-5-sonnet-latest': 21.6, # output 8192 tokens
    'claude-3-5-haiku-latest': 5.76, # no vision and output 8192 tokens
    'claude-3-opus-latest': 108, # 4096 tokens
    # Old:
    'claude-3-sonnet-20240229': 21.6, # 4096 tokens
    'claude-3-haiku-20240307': 1.8, # 200K context window

    }


