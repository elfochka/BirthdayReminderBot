import os
from dotenv import set_key

bot_token = os.environ.get('BOT_TOKEN')
host = os.environ.get('HOST')
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')
database = os.environ.get('DATABASE')

set_key('.env', 'BOT_TOKEN', bot_token)
set_key('.env', 'HOST', host)
set_key('.env', 'USER', user)
set_key('.env', 'PASSWORD', password)
set_key('.env', 'DATABASE', database)
