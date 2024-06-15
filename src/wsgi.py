from os import getenv
from gevent import monkey

monkey.patch_all()

import logging
from app import init_app, socketio

env = getenv("FLASK_ENV", "testing")

if env == "testing":
    app = init_app("config.TestingConfig")
else:
    app = init_app("config.ProductionConfig")

if __name__ != "__main__":
    logging.info("Starting app...")
