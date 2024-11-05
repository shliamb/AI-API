import os
from dotenv import load_dotenv
load_dotenv()

TOKEN_TELEGRAM = os.environ.get('TELEGRAM_BOT_AI_API_KEY') # Telegram key
API_KEY_OPENAI = os.environ.get('OPENAI_API_KEY') # OpenAI key-token - установить только на сервере руками
API_KEY_GEMINI = os.environ.get('GEMINI_KEY')
API_KEY_CLAUDE = os.environ.get('CLAUDE_KEY')
USER_DB = os.environ.get('USER_DB')
PASWORD_DB = os.environ.get('PASWOR_DB')
IS_ADMIN = int(os.environ.get('ADMIN'))

