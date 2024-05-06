import logging
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt

from db import DB
from utils.log import set_up_logger
from utils.mongo_json_provider import MongoJSONProvider
from routes.health_routes import health_bp
from routes.user_routes import user_bp
from routes.authentication_routes import auth_bp
from routes.document_routes import document_bp
from sockets.connection import handle_connections
from sockets.chat import handle_chat
from sockets.comment import handle_comments
from sockets.annotation import handle_annotations


socketio = SocketIO()
bcrypt = Bcrypt()


def init_app(config_path: str):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_path)
    app.json = MongoJSONProvider(app)

    socketio.init_app(app, cors_allowed_origins="*")
    bcrypt.init_app(app)
    CORS(app)

    debug = app.config.get('MONGO_HOST', True)
    set_up_logger(debug, 'log.txt')

    with app.app_context():
        db = DB()
        db.connect()

        # Set up WebSocket handlers
        handle_connections(socketio)
        handle_chat(socketio)
        handle_comments(socketio)
        handle_annotations(socketio)

        # Connect API blueprints
        app.register_blueprint(health_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(document_bp)

        return app


if __name__ == '__main__':
    app = init_app("config.DevelopmentConfig")
    logging.info('Starting app...')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
