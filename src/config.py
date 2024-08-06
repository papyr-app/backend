from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION = getenv("AWS_DEFAULT_REGION")
    S3_BUCKET_NAME = getenv("S3_BUCKET_NAME")
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    # Overwrite database URI and use in-memory database instead
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    DEBUG = False
