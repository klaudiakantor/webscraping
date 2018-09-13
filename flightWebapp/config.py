from dotenv import load_dotenv
import os

class Config(object):
    def __init__(self):
        env_path = os.path.join(os.getcwd(), '.env')
        load_dotenv(dotenv_path=env_path)

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_USER = os.getenv("DATABASE_USER")
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + DATABASE_USER + ':' + DATABASE_PASSWORD + '@localhost:5432/flights'
