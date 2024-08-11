import os
from dotenv import load_dotenv
load_dotenv()

token_telegram = os.environ.get('TELEGRAM_BOT_CHATGPT_API_KEY') # Telegram key
api_key_openai = os.environ.get('CHATGPT_API_KEY') # OpenAI key-token - установить только на сервере руками
my_key = os.environ.get('MY_KEY')
# white_list = os.environ.get('WHITE_LIST')
# admin_user_ids = os.environ.get('ADMIN_USER_IDS')
# block = os.environ.get('ALLOWED_TELEGRAM_USER_IDS')
# oppas = os.environ.get('OPPAS')
# user_db = os.environ.get('USER_DB')
# paswor_db = os.environ.get('PASWOR_DB')