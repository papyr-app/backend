from flask import Flask
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from src.utils.log import set_up_logger

app = Flask(__name__)
socketio = SocketIO(app)
bcrypt = Bcrypt(app)
CORS(app)


@app.route('/')
def index():
    return "Hello, World!"


def main():
    set_up_logger(True, "log.txt")
    socketio.run(app)


if __name__ == '__main__':
    main()
