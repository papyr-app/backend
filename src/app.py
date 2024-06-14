from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from file_manager.s3_client import S3Client
from utils.log import set_up_logger

db = SQLAlchemy()
bcrypt = Bcrypt()
socketio = SocketIO(async_mode="gevent")


def init_app(config_path: str):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_path)

    socketio.init_app(app, cors_allowed_origins="*")
    bcrypt.init_app(app)
    db.init_app(app)
    CORS(app)

    if not app.config.get("SECRET_KEY"):
        raise ValueError("SECRET_KEY must be set")

    if not app.config.get("S3_BUCKET_NAME"):
        raise ValueError("S3_BUCKET_NAME must be set")

    debug = app.config.get("DEBUG", True)
    set_up_logger(debug, "log.txt")

    s3_bucket_name = app.config["S3_BUCKET_NAME"]
    s3_client = S3Client(s3_bucket_name)

    with app.app_context():
        db.create_all()

        # Import and register sockets
        from sockets.connection_socket import handle_connections
        from sockets.chat_socket import handle_chat
        from sockets.comment_socket import handle_comments
        from sockets.annotation_socket import handle_annotations

        handle_connections(socketio)
        handle_chat(socketio)
        handle_comments(socketio)
        handle_annotations(socketio)

        # Import and register blueprints
        from routes.health_routes import create_health_bp
        from routes.user_routes import create_user_bp
        from routes.authentication_routes import create_auth_bp
        from routes.pdf_document_routes import create_document_bp
        from routes.invitation_routes import create_invitation_bp

        health_bp = create_health_bp()
        user_bp = create_user_bp()
        auth_bp = create_auth_bp()
        document_bp = create_document_bp(s3_client)
        invitation_bp = create_invitation_bp()

        app.register_blueprint(health_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(document_bp)
        app.register_blueprint(invitation_bp)

    return app
