import logging
from flask import request, jsonify, send_file, Blueprint
from marshmallow import ValidationError

from src.file_manager.ifile_manager import IFileManager
from src.errors import AuthorizationError
from src.auth.decorators import token_required
from src.services.pdf_document_service import PDFDocumentService
from src.services.user_service import UserService
from src.schemas.pdf_document_schema import PDFDocumentSchema
from src.models import User


def create_document_bp(file_manager: IFileManager):
    document_bp = Blueprint("document", __name__, url_prefix="/documents")

    @document_bp.route("/<document_id>", methods=["GET"])
    @token_required
    def get_document(user: User, document_id: str):
        try:
            pdf_document = PDFDocumentService.get_pdf_document_by_id(document_id)
            PDFDocumentService.check_user_access(pdf_document, user.id)
            schema = PDFDocumentSchema(context={"user": user})
            return jsonify({"data": schema.dump(pdf_document)}), 200
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except AuthorizationError as err:
            return jsonify({"error": str(err)}), 403
        except Exception as err:
            logging.error("Error getting PDF document: %s", str(err))
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    @document_bp.route("/<document_id>/download", methods=["GET"])
    @token_required
    def download_document(user: User, document_id: str):
        try:
            pdf_document = PDFDocumentService.get_pdf_document_by_id(document_id)
            PDFDocumentService.check_user_access(pdf_document, user.id)
            document_key = f"{str(pdf_document.id)}.pdf"

            if not file_manager.file_exists(document_key):
                return jsonify({"error": "File not found"}), 404

            file_stream = file_manager.download_file(document_key)
            if not file_stream:
                return jsonify({"error": "File not found"}), 404

            return send_file(
                file_stream, download_name=document_key, as_attachment=True
            )
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except AuthorizationError as err:
            return jsonify({"error": str(err)}), 403
        except Exception as err:
            logging.error("Error dowloading PDF document: %s", str(err))
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

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
            document = PDFDocumentService.create_pdf_document(data, user.id)
            document_key = f"{str(document.id)}.pdf"
            upload_succeeded = file_manager.upload_file(file, document_key)
            if upload_succeeded:
                schema = PDFDocumentSchema(context={"user": user}).dump(document)
                return jsonify({"data": schema}), 201
            else:
                PDFDocumentService.delete_pdf_document(document.id, user.id)
                return jsonify({"error": "Upload failed"}), 500
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except Exception as err:
            logging.error("Error creating PDF document: %s", str(err))
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    @document_bp.route("/<document_id>", methods=["PATCH"])
    @token_required
    def update_document(user: User, document_id: str):
        data = request.get_json()
        try:
            pdf_document = PDFDocumentService.get_pdf_document_by_id(document_id)
            PDFDocumentService.check_user_access(pdf_document, user.id)
            updated_document = PDFDocumentService.update_pdf_document(
                pdf_document, data, user.id
            )
            schema = PDFDocumentSchema(context={"user": user}).dump(updated_document)
            return jsonify({"data": schema}), 200
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except AuthorizationError as err:
            return jsonify({"error": str(err)}), 403
        except Exception as err:
            logging.error("Error updating PDF document: %s", str(err))
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    @document_bp.route("/<document_id>", methods=["DELETE"])
    @token_required
    def delete_document(user: User, document_id: str):
        try:
            pdf_document = PDFDocumentService.get_pdf_document_by_id(document_id)
            PDFDocumentService.check_user_access(pdf_document, user.id)
            document_key = f"{str(pdf_document.id)}.pdf"

            if not file_manager.file_exists(document_key):
                return jsonify({"error": "File not found"}), 404

            delete_succeeded = file_manager.delete_file(document_key)

            if delete_succeeded:
                PDFDocumentService.delete_pdf_document(pdf_document)
                return jsonify({"data": "Document deleted successfully"}), 200
            else:
                return jsonify({"error": "Failed to delete document"}), 500
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except AuthorizationError as err:
            return jsonify({"error": str(err)}), 403
        except Exception as err:
            logging.error("Error deleting PDF document: %s", str(err))
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    @document_bp.route("/<document_id>/add_collaborator", methods=["POST"])
    @token_required
    def add_collaborator(user: User, document_id: str):
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"error": "Missing required field"}), 400

        try:
            pdf_document = PDFDocumentService.get_pdf_document_by_id(document_id)
            PDFDocumentService.check_user_access(pdf_document, user.id)
            collaborator = UserService.get_user_by_email(email)
            PDFDocumentService.add_collaborator(pdf_document, collaborator)
            return jsonify({"data": "Collaborator added"}), 200
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except AuthorizationError as err:
            return jsonify({"error": str(err)}), 403
        except Exception as err:
            logging.error("Error adding collaborator: %s", str(err))
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    @document_bp.route("/<document_id>/remove_collaborator", methods=["POST"])
    @token_required
    def remove_collaborator(user: User, document_id: str):
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"error": "Missing required field"}), 400

        try:
            pdf_document = PDFDocumentService.get_pdf_document_by_id(document_id)
            PDFDocumentService.check_user_access(pdf_document, user.id)
            collaborator = UserService.get_user_by_email(email)
            PDFDocumentService.remove_collaborator(pdf_document, collaborator)
            return jsonify({"data": "Collaborator removed"}), 200
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except AuthorizationError as err:
            return jsonify({"error": str(err)}), 403
        except Exception as err:
            logging.error("Error removing collaborator: %s", str(err))
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    @document_bp.route("/share/<share_token>", methods=["POST"])
    @token_required
    def use_share_token(user: User, share_token: str):
        try:
            pdf_document = PDFDocumentService.get_pdf_document_by_share_token(
                share_token
            )
            if not pdf_document.can_share:
                raise ValidationError("Document is not shareable.")
            PDFDocumentService.add_collaborator(pdf_document, user)
            return jsonify({"data": "User added as collaborator"}), 200
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except Exception as err:
            logging.error("Error using share token: %s", str(err))
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    return document_bp
