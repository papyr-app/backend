from gevent import monkey

monkey.patch_all()

import logging
from app import init_app, socketio


if __name__ == "__main__":
    app = init_app("config.DevelopmentConfig")
    logging.info("Starting app...")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
