import logging
from urllib.parse import urlparse, parse_qs
from functools import wraps
from flask_socketio import emit, disconnect
from flask import request, jsonify
from marshmallow.exceptions import ValidationError

from src.auth.jwt_handler import decode_jwt
from src.services.user_service import UserService


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Missing token"}), 403

        try:
            user_id = decode_jwt(token)
            if not user_id:
                return jsonify({"error": "Token is invalid"}), 403
            current_user = UserService.get_user_by_id(user_id)
        except ValidationError as err:
            return jsonify({"error": str(err)}), 402
        except Exception as err:
            logging.error("Error decoding JWT: %s", str(err))
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

        return f(current_user, *args, **kwargs)

    return decorated


def token_required_socket(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        query_params = parse_qs(urlparse(request.url).query)
        token = query_params.get("token", [None])[0]
        room = query_params.get("room", [None])[0]

        if not token or not room:
            emit("error", {"message": "Missing token or room in request."})
            disconnect()
            return

        try:
            user_id = decode_jwt(token)
            if not user_id:
                emit("error", {"error": "Token is invalid"})
                disconnect()
                return
            current_user = UserService.get_user_by_id(user_id)
        except ValidationError as err:
            emit("error", {"error": str(err)})
            disconnect()
            return
        except Exception as err:
            logging.error("Error decoding JWT: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"error": "Internal error"})
            disconnect()
            return

        return f(current_user, room, *args, **kwargs)

    return decorated
