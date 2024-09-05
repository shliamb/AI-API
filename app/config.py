
#### CONFIG ####

limit_trying = 5
timeout_after_error_username = 5 # sec.
waiting_time = 15 # min/
time_correction = +3 # Moscow



# Prices per 1M tokens:

price = { 
    'chatgpt-4o-latest': 40,
    'gpt-4o': 40, 
    'gpt-4o-2024-08-06': 25,
    'gpt-4o-2024-05-13': 40,
    'gpt-4o-mini': 1.5, # no vision
    'gpt-4o-mini-2024-07-18': 1.5,
    'gpt-4-turbo-2024-04-09': 80,
    'DALL·E 3': 0.08,
    }




"""

5Sep2024 OpenAI:

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