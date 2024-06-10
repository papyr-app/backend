from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_HOST = getenv("MONGO_HOST", "localhost")
    MONGO_NAME = getenv("MONGO_NAME", "papyr")
    MONGO_USER = getenv("MONGO_USER")
    MONGO_PASS = getenv("MONGO_PASS")

    AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION = getenv("AWS_DEFAULT_REGION")
    S3_BUCKET_NAME = getenv("S3_BUCKET_NAME")

    SECRET_KEY = getenv("SECRET_KEY")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
