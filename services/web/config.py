from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    FLASK_ENV = environ.get('FLASK_ENV')
    DEBUG = True if FLASK_ENV == 'development' else False
    TESTING = True if FLASK_ENV == 'development' else False

    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FORLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
