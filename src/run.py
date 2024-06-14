from os import getenv
from gevent import monkey

monkey.patch_all()

import logging
from app import init_app, socketio


if __name__ == "__main__":
    env = getenv("FLASK_ENV", "development")

    if env == "development":
        app = init_app("config.DevelopmentConfig")
    elif env == "testing":
        app = init_app("config.TestingConfig")
    else:
        app = init_app("config.ProductionConfig")

    logging.info(f"Starting app in {env} mode...")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
