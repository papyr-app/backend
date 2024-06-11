import logging
from flask import request, jsonify, send_file, Blueprint
from marshmallow import ValidationError

from file_manager.ifile_manager import IFileManager
from errors import AuthorizationError
from auth.decorators import token_required
from services.pdf_document_service import PDFDocumentService
from services.user_service import UserService
from models import User


def create_document_bp(file_manager: IFileManager):
    document_bp = Blueprint("document", __name__, url_prefix="/api/documents")

    @document_bp.route("/<document_id>", methods=["GET"])
    @token_required
    def get_document(user: User, document_id: int):
        try:
            document = PDFDocumentService.get_pdf_document_by_id(document_id)
            return jsonify({"data": document}), 200
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except AuthorizationError as e:
            return jsonify({"error": str(e)}), 403
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    @document_bp.route("/<document_id>/download", methods=["GET"])
    @token_required
    def download_document(user: User, document_id: str):
        try:
            document = PDFDocumentService.get_pdf_document_by_id(document_id)
            document_key = f"{str(document.id)}.pdf"

            if not file_manager.file_exists(document_key):
                return jsonify({"error": "File not found"}), 404

            file_stream = file_manager.download_file(document_key)
            if not file_stream:
                return jsonify({"error": "File not found"}), 404

            return send_file(
                file_stream, download_name=document_key, as_attachment=True
            )
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except AuthorizationError as e:
            return jsonify({"error": str(e)}), 403
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    @document_bp.route("", methods=["POST"])
    @token_required
    def create_document(user: User):
        file = request.files.get("file")
        data = request.form

        if not file:
            return jsonify({"error": "Missing file"}), 400

        if not file.filename.endswith(".pdf"):
            return jsonify({"error": "Only PDF files are allowed"}), 400

        try:
            document = PDFDocumentService.create_pdf_document(data)
            document_key = f"{str(document.id)}.pdf"
            upload_succeeded = file_manager.upload_file(file, document_key)

            # TODO virtual path

            if upload_succeeded:
                return jsonify({"data": document}), 201
            else:
                PDFDocumentService.delete_pdf_document(document.id)
                return jsonify({"error": "Upload failed"}), 500
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    @document_bp.route("/<document_id>", methods=["PATCH"])
    @token_required
    def update_document(user: User, document_id: int):
        data = request.get_json()
        try:
            updated_document = PDFDocumentService.update_pdf_document(document_id, data)
            return jsonify({"data": updated_document}), 201
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except AuthorizationError as e:
            return jsonify({"error": str(e)}), 403
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    @document_bp.route("/<document_id>", methods=["DELETE"])
    @token_required
    def delete_document(user: User, document_id: int):
        try:
            document = PDFDocumentService.get_pdf_document_by_id(document_id)
            file_path = document.file_path

            if not file_manager.file_exists(file_path):
                return jsonify({"error": "File not found"}), 404

            delete_succeeded = file_manager.delete_file(file_path)

            if delete_succeeded:
                PDFDocumentService.delete_pdf_document(document_id)
                return jsonify({"data": "Document deleted successfully"}), 200
            else:
                return jsonify({"error": "Failed to delete document"}), 500
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except AuthorizationError as e:
            return jsonify({"error": str(e)}), 403
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    @document_bp.route("/<document_id>/add_collaborator", methods=["POST"])
    @token_required
    def add_collaborator(user: User, document_id: int):
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"error": "Missing required field"}), 400

        try:
            collaborator = UserService.get_user_by_email(email)
            PDFDocumentService.add_collaborator(document_id, user.id, collaborator.id)
            return jsonify({"data": "Collaborator added"}), 201
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except AuthorizationError as e:
            return jsonify({"error": str(e)}), 403
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    @document_bp.route("/<document_id>/remove_collaborator", methods=["POST"])
    @token_required
    def remove_collaborator(user: User, document_id: int):
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"error": "Missing required field"}), 400

        try:
            collaborator = UserService.get_user_by_email(email)
            PDFDocumentService.remove_collaborator(
                document_id, user.id, collaborator.id
            )
            return jsonify({"data": "Collaborator removed"}), 201
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except AuthorizationError as e:
            return jsonify({"error": str(e)}), 403
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    @document_bp.route("/share/<share_token>", methods=["POST"])
    @token_required
    def use_share_token(user: User, share_token: str):
        try:
            document = PDFDocumentService.get_pdf_document_by_share_token(
                share_token, user.id
            )
            PDFDocumentService.add_collaborator(document.id, user.id, document.owner.id)
            return jsonify({"data": "User added as collaborator"}), 201
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logging.error(e)
            return jsonify({"error": str(e)}), 500

    return document_bp
