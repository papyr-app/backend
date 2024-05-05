from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_HOST = getenv('MONGO_HOST', 'localhost')
    MONGO_NAME = getenv('MONGO_NAME', 'papyr')
    MONGO_USER = getenv('MONGO_USER')
    MONGO_PASS = getenv('MONGO_PASS')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
