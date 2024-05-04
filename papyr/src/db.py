import os
import logging
from urllib.parse import quote_plus
from mongoengine import connect


class DB:
    """
    MongoEngine database instance and methods
    """

    @staticmethod
    def connect(db_name: str = None):
        db_host = os.getenv("MONGO_HOST") or "mongo"
        db_user = os.getenv("MONGO_USER") or None
        db_pass = os.getenv("MONGO_PASS") or None

        if db_user:
            db_user_quote = quote_plus(db_user)
            db_pass_quote = quote_plus(db_pass)
            mongo_uri = f"mongodb+srv://{db_user_quote}:{db_pass_quote}@{db_host}"
        else:
            mongo_uri = f"mongodb://{db_host}"

        logging.info(f"Connecting to database host {db_host}...")
        connect(db_name, host=mongo_uri)
