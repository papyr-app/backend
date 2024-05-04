from flask import Flask
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from src.db import DB
from src.utils.log import set_up_logger

app = Flask(__name__)
socketio = SocketIO(app)
bcrypt = Bcrypt(app)
CORS(app)


def main():
    DB.connect("papyr")
    set_up_logger(True, "log.txt")
    socketio.run(app)


if __name__ == '__main__':
    main()
