from functools import wraps
from flask_socketio import disconnect
from flask import request, jsonify

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
        except Exception as err:
            return jsonify({"error": str(err)}), 403

        return f(current_user, *args, **kwargs)

    return decorated


def token_required_socket(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not args:
            disconnect()
            return jsonify({"error": "Missing arguments"}), 403

        data = args[0]
        token = data.get('token')
        if not token:
            disconnect()
            return jsonify({"error": "Missing token"}), 403

        try:
            user_id = decode_jwt(token)
            if not user_id:
                disconnect()
                return jsonify({"error": "Token is invalid"}), 403
            current_user = UserService.get_user_by_id(user_id)
        except Exception as err:
            disconnect()
            return jsonify({"error": str(err)}), 403

        return f(current_user, *args, **kwargs)
    return decorated
