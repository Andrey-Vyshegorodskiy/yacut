import os
import re
import string

ORIGINAL_LEN = 2048
SHORT_LEN = 16
CUSTOM_ID_LEN = 6
CHARACTERS_SET = string.ascii_letters + string.digits
PATTERN = f'[{re.escape(CHARACTERS_SET)}]'

ITERATIONS_COUNT = 100


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    # тесты требуют, чтобы значение по умолчаю было 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='my_secret_key')
