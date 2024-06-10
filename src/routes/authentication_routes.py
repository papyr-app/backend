import logging
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from mongoengine.errors import NotUniqueError, DoesNotExist
from marshmallow import ValidationError

from auth.jwt_handler import generate_jwt
from services import user_service
from schemas.user_schema import CreateUserSchema
from schemas.login_schema import LoginSchema


def create_auth_bp(bcrypt: Bcrypt):
    auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

    @auth_bp.route("/register", methods=["POST"])
    def register():
        data = request.json
        schema = CreateUserSchema()

        try:
            validated_data = schema.load(data)
            user = user_service.create_user(**validated_data)
            return jsonify({"data": user.to_mongo().to_dict()}), 201
        except NotUniqueError as e:
            return jsonify({"error": str(e)}), 400
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    @auth_bp.route("/login", methods=["POST"])
    def login():
        data = request.json
        schema = LoginSchema()
        try:
            validated_data = schema.load(data)
            user = user_service.get_user_by_username(validated_data["username"])
            if user.check_password(validated_data["password"]):
                user.record_login()
                jwt = generate_jwt(str(user.id))
                return jsonify({"data": jwt}), 200
            else:
                return jsonify({"error": "Invalid username or password"}), 401
        except DoesNotExist:
            return jsonify({"error": "Invalid username or password"}), 401
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    return auth_bp
