from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION = getenv("AWS_DEFAULT_REGION")
    S3_BUCKET_NAME = getenv("S3_BUCKET_NAME")

    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = getenv("SECRET_KEY")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
