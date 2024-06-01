import logging
from urllib.parse import quote_plus
from flask import current_app
from mongoengine import connect


class DB:
    """
    MongoEngine database instance
    """

    def __init__(self):
        self.db_host = current_app.config.get('MONGO_HOST')
        self.db_name = current_app.config.get('MONGO_NAME')
        self.db_user = current_app.config.get('MONGO_USER')
        self.db_pass = current_app.config.get('MONGO_PASS')

    def connect(self):
        if self.db_user:
            db_user_quote = quote_plus(self.db_user)
            db_pass_quote = quote_plus(self.db_pass)
            mongo_uri = f"mongodb+srv://{db_user_quote}:{db_pass_quote}@{self.db_host}"
        else:
            mongo_uri = f"mongodb://{self.db_host}"

        logging.info(f"Connecting to database host {self.db_host}...")
        connect(self.db_name, host=mongo_uri)
