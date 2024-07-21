import logging
from flask import request, jsonify, Blueprint
from marshmallow import ValidationError

from src.auth.decorators import token_required
from src.services.user_service import UserService
from src.services.pdf_document_service import PDFDocumentService
from src.models import User
from src.schemas.user_schema import UserSchema
from src.schemas.pdf_document_schema import PDFDocumentSchema


def create_user_bp():
    user_bp = Blueprint("user", __name__, url_prefix="/users")

    @user_bp.route("", methods=["GET"])
    @token_required
    def get_user(user: User):
        try:
            user = UserService.get_user_by_id(user.id)
            return jsonify({"data": UserSchema().dump(user)}), 200
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except Exception as err:
            logging.error("Error getting user: %s", str(err))
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    @user_bp.route("", methods=["PATCH"])
    @token_required
    def update_user(user: User):
        data = request.get_json()
        try:
            user = UserService.update_user(user.id, data)
            return jsonify({"data": UserSchema().dump(user)}), 200
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except Exception as err:
            logging.error("Error updating user: %s", str(err))
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    @user_bp.route("/documents", methods=["GET"])
    @token_required
    def get_documents(user: User):
        try:
            documents = PDFDocumentService.get_documents_by_user(user.id)
            return jsonify({"data": PDFDocumentSchema(many=True).dump(documents)}), 200
        except Exception as err:
            logging.error("Error getting user documents: %s", str(err))
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    return user_bp
