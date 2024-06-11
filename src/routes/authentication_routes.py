import logging
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from services.user_service import UserService


def create_auth_bp():
    auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

    @auth_bp.route("/register", methods=["POST"])
    def register():
        data = request.json
        try:
            user = UserService.create_user(data)
            return jsonify({"data": user}), 201
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    @auth_bp.route("/login", methods=["POST"])
    def login():
        data = request.json
        try:
            jwt = UserService.login(data)
            return jsonify({"jwt": jwt}), 200
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    return auth_bp
