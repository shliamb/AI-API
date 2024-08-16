import os
from dotenv import load_dotenv
load_dotenv()

token_telegram = os.environ.get('TELEGRAM_BOT_CHATGPT_API_KEY') # Telegram key
api_key_openai = os.environ.get('CHATGPT_API_KEY') # OpenAI key-token - установить только на сервере руками
my_key = os.environ.get('MY_KEY')
