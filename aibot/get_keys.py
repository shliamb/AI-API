import os
from dotenv import load_dotenv
load_dotenv()


TELEGRAM_BOT_TOKEN = os.environ.get('telegram_bot_token')

ACCESS_ID = str(os.environ.get('access_id'))
KEY_API_AI = str(os.environ.get('key_api_ai'))
VALUE_KEY_API_AI = str(os.environ.get('value_key_api_ai'))

USER_DB = os.environ.get('USER_DB')
PASSWORD_DB = os.environ.get('PASSWORD_DB')
DB_NAME = os.environ.get('DB_NAME')

ADMIN_ID = int(os.environ.get('admin_id'))

KEY_API_DEEPSEEK = os.environ.get('key_api_deepseek')

