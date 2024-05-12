from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt

from db import DB
from file_manager.s3_client import S3Client
from utils.log import set_up_logger
from utils.mongo_json_provider import MongoJSONProvider
from routes.health_routes import create_health_bp
from routes.user_routes import create_user_bp
from routes.authentication_routes import create_auth_bp
from routes.document_routes import create_document_bp
from routes.file_routes import create_file_blueprint
from sockets.connection_socket import handle_connections
from sockets.chat_socket import handle_chat
from sockets.comment_socket import handle_comments
from sockets.annotation_socket import handle_annotations


socketio = SocketIO(async_mode='gevent')
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

    s3_bucket_name = app.config['S3_BUCKET_NAME']
    s3_client = S3Client(s3_bucket_name)

    with app.app_context():
        db = DB()
        db.connect()

        handle_connections(socketio)
        handle_chat(socketio)
        handle_comments(socketio)
        handle_annotations(socketio)

        health_bp = create_health_bp()
        user_bp = create_user_bp()
        auth_bp = create_auth_bp(bcrypt)
        document_bp = create_document_bp()
        file_bp = create_file_blueprint(s3_client)
        app.register_blueprint(health_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(document_bp)
        app.register_blueprint(file_bp)

        return app
