import os

# api
API_KEY = 'NzA5NzEyMTY1MDExMTkzODg3.Xuo5qQ.cJpYOCyekMCkZRiYIyj3NNaRZCI'

# base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# debug
DEBUG_MODE = True

# application
APPLICATION_MODULE = 'apps'
APPLICATION_DIR = os.path.join(BASE_DIR, APPLICATION_MODULE)

# redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# db (mysql)
DATABASE_HOST = 'localhost'
DATABASE_PORT = 3306
DATABASE_USER = 'root'
DATABASE_PASSWORD = '1111'
DATABASE_SCHEMA_NAME = 'ebot'
