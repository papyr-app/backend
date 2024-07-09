import logging
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from src.services.user_service import UserService
from src.schemas.user_schema import UserSchema


def create_auth_bp():
    auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

    @auth_bp.route("/register", methods=["POST"])
    def register():
        data = request.json
        try:
            user = UserService.create_user(data)
            return jsonify({"data": UserSchema().dump(user)}), 201
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except Exception as err:
            logging.error(f"Error registering user: {str(err)}")
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    @auth_bp.route("/login", methods=["POST"])
    def login():
        data = request.json
        try:
            jwt = UserService.login(data)
            return jsonify({"data": jwt}), 200
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except Exception as err:
            logging.error(f"Error logging in: {str(err)}")
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    return auth_bp
