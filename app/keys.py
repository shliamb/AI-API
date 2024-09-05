import os
from dotenv import load_dotenv
load_dotenv()

token_telegram = os.environ.get('TELEGRAM_BOT_AI_API_KEY') # Telegram key
api_key_openai = os.environ.get('OPENAI_API_KEY') # OpenAI key-token - установить только на сервере руками
user_db = os.environ.get('USER_DB')
paswor_db = os.environ.get('PASWOR_DB')
is_admin = int(os.environ.get('ADMIN'))
api_key_gemini = os.environ.get('GEMINI_KEY')

