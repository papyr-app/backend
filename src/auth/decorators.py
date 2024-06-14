from functools import wraps
from flask import request, jsonify
from auth.jwt_handler import decode_jwt

from services.user_service import UserService


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
        except Exception as e:
            return jsonify({"error": str(e)}), 403

        return f(current_user, *args, **kwargs)

    return decorated
