import logging
from urllib.parse import quote_plus
from flask import current_app
from mongoengine import connect


class DB:
    """
    MongoEngine database instance
    """

    def connect():
        db_host = current_app.config.get('MONGO_HOST')
        db_name = current_app.config.get('MONGO_NAME')
        db_user = current_app.config.get('MONGO_USER')
        db_pass = current_app.config.get('MONGO_PASS')

        if db_user:
            db_user_quote = quote_plus(db_user)
            db_pass_quote = quote_plus(db_pass)
            mongo_uri = f"mongodb+srv://{db_user_quote}:{db_pass_quote}@{db_host}"
        else:
            mongo_uri = f"mongodb://{db_host}"

        logging.info(f"Connecting to database host {db_host}...")
        connect(db_name, host=mongo_uri)
