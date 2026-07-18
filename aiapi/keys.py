import os
from dotenv import load_dotenv

'''
    из .env
'''

load_dotenv()

TOKEN_TELEGRAM = os.environ.get('TELEGRAM_BOT_AI_API_KEY')
#TOKEN_TELEGRAM = os.environ.get('TOKEN_TELEGRAM').encode().decode('unicode_escape')
API_KEY_OPENAI = os.environ.get('OPENAI_API_KEY')
API_KEY_GEMINI = os.environ.get('GEMINI_KEY')
API_KEY_CLAUDE = os.environ.get('CLAUDE_KEY')
API_KEY_GROK = os.environ.get('GROK_KEY')
USER_DB = os.environ.get('USER_DB')
DB_NAME = os.environ.get('DB_NAME')
PASSWORD_DB = os.environ.get('PASSWORD_DB')
IS_ADMIN = int(os.environ.get('ADMIN'))

