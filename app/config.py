
#### CONFIG ####

limit_trying = 5
timeout_after_error_username = 5 # sec.
waiting_time = 15 # min/
time_correction = +3 # Moscow
money_to_start = 1 # 1$ to start work
my_app_key = "appkey" # Key to API Key
min_pay = 1 # Minimum pay 


# Prices per 1M tokens:
price = {
    # OpenAI:
    'chatgpt-4o-latest': 40,
    'gpt-4o': 40, 
    'gpt-4o-2024-08-06': 25,
    'gpt-4o-2024-05-13': 40,
    'gpt-4o-mini': 1.5, # no vision
    'gpt-4o-mini-2024-07-18': 1.5, # no vision
    'gpt-4-turbo-2024-04-09': 80,
    # Images:
    'DALL·E 3': 0.08,
    # Google Gemini:
    'gemini-1.5-flash-latest': 1.125,
    'gemini-1.5-pro-latest': 93.75,
    # 'gemini-1.0-pro-latest': 4,
    'text-embedding-004': 0,
    # 'aqa': 0,
    }










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




Model         Quality           Resolution       Price     

DALL·E 3      Standart          1024*1024        0.04$/image



Model         Usage $

Whisper       0.006/minute (rounded to the nearest second)
TTS           15/1M characters
TTS HD        30/1M characters


"""