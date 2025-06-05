import os
from dotenv import load_dotenv

'''
    из .env
'''

load_dotenv()

USER_DB = os.environ.get('USER_DB')
PASSWORD_DB = os.environ.get('PASSWORD_DB')
ADMIN_ID = int(os.environ.get('ADMIN_ID'))
DB_NAME = os.environ.get('DB_NAME')
TOKEN_TELEGRAM = os.environ.get('TOKEN_TELEGRAM').encode().decode('unicode_escape')
#TOKEN_TELEGRAM = os.environ.get('TOKEN_TELEGRAM') 