from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt

from db import DB
from utils.log import set_up_logger
from routes.health_routes import health_bp
from routes.user_routes import user_bp
from routes.authentication_routes import auth_bp
from sockets.chat import handle_chat


socketio = SocketIO()
bcrypt = Bcrypt()
db = DB()


def init_app():
    set_up_logger(True, "log.txt")

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    socketio.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    db.connect()

    handle_chat(socketio)

    with app.app_context():
        app.register_blueprint(health_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(auth_bp)

        return app


if __name__ == '__main__':
    app = init_app()
    socketio.run(app, host='0.0.0.0', port=5000)
