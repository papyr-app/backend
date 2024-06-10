from gevent import monkey

monkey.patch_all()

import logging
from app import init_app, socketio

app = init_app("config.ProductionConfig")

if __name__ != "__main__":
    logging.info("Starting app...")
