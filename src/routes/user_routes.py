import logging
from flask import request, jsonify, Blueprint
from marshmallow import ValidationError

from auth.decorators import token_required
from services.user_service import UserService
from services.pdf_document_service import PDFDocumentService
from schemas.user_schema import UpdateUserSchema
from models.user import User


def create_user_bp():
    user_bp = Blueprint("user", __name__, url_prefix="/api/users")

    @user_bp.route("", methods=["GET"])
    @token_required
    def get_user(user: User):
        try:
            user = UserService.get_user_by_id(user.id)
            return jsonify({"data": user}), 200
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    @user_bp.route("", methods=["PATCH"])
    @token_required
    def update_user(user: User):
        data = request.get_json()
        try:
            user = UserService.update_user(user.id, data)
            return jsonify({"data": user}), 200
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    @user_bp.route("/documents", methods=["GET"])
    @token_required
    def get_documents(user: User):
        try:
            documents = PDFDocumentService.get_documents_by_user(user.id)
            return jsonify({"data": documents}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    return user_bp
