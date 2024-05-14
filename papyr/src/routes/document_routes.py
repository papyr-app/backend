import logging
from flask import request, jsonify, Blueprint
from mongoengine.errors import DoesNotExist, NotUniqueError
from marshmallow import ValidationError

from errors import AuthorizationError
from auth.decorators import token_required
from services import document_service
from services import user_service
from models.user import User
from models.pdf_document import PDFDocument
from schemas.pdf_document_schema import CreatePDFDocumentSchema, UpdatePDFDocumentSchema


def create_document_bp():
    document_bp = Blueprint('document', __name__, url_prefix='/api/documents')

    @document_bp.route('/<document_id>', methods=['GET'])
    @token_required
    def get_document(user: User, document_id: int):
        try:
            document = document_service.get_document_check_access(document_id, user.id)
            return jsonify({'data': document.to_mongo().to_dict()}), 200
        except DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except AuthorizationError as e:
            return jsonify({'error': str(e)}), 403
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    @document_bp.route('/', methods=['POST'])
    @token_required
    def create_document(user: User):
        data = request.get_json()
        try:
            schema = CreatePDFDocumentSchema()
            validated_data = schema.load(data)
            document = document_service.create_document(
                    str(user.id),
                    **validated_data
            )
            return jsonify({'data': document.to_mongo().to_dict()}), 201
        except NotUniqueError:
            return jsonify({'error': 'Document already exists'}), 409
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    @document_bp.route('/<document_id>', methods=['PATCH'])
    @token_required
    def update_document(user: User, document_id: int):
        data = request.get_json()
        try:
            schema = CreatePDFDocumentSchema()
            validated_data = schema.load(data)
            document = document_service.get_document_check_access(document_id, user.id)
            document = document_service.update_document(document, validated_data)
            return jsonify({'data': document.to_mongo().to_dict()}), 201
        except DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except AuthorizationError as e:
            return jsonify({'error': str(e)}), 403
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    @document_bp.route('/<document_id>', methods=['DELETE'])
    @token_required
    def delete_document(user: User, document_id: int):
        try:
            document = document_service.get_document_check_access(document_id, user.id)
            document_service.delete_document(document)
            return jsonify({'data': 'Document deleted successfully'}), 200
        except DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except AuthorizationError as e:
            return jsonify({'error': str(e)}), 403
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    @document_bp.route('/<document_id>/add_collaborator', methods=['POST'])
    @token_required
    def add_collaborator(user: User, document_id: int):
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({'error': 'Missing required field'}), 400

        try:
            document = document_service.get_document_check_access(document_id, user.id)
            user = user_service.get_user_by_email(email)
            document_service.add_collaborator(user, document)
            return jsonify({'data': 'Collaborator added'}), 201
        except PDFDocument.DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except User.DoesNotExist:
            return jsonify({'error': 'User not found'}), 404
        except AuthorizationError as e:
            return jsonify({'error': str(e)}), 403
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    @document_bp.route('/<document_id>/remove_collaborator', methods=['POST'])
    @token_required
    def remove_collaborator(user: User, document_id: int):
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({'error': 'Missing required field'}), 400

        try:
            document = document_service.get_document_check_access(document_id, user.id)
            user = user_service.get_user_by_email(email)
            document_service.remove_collaborator(user, document)
            return jsonify({'data': 'Collaborator removed'}), 201
        except PDFDocument.DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except User.DoesNotExist:
            return jsonify({'error': 'User not found'}), 404
        except AuthorizationError as e:
            return jsonify({'error': str(e)}), 403
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    @document_bp.route('/<document_id>/share', methods=['GET'])
    @token_required
    def get_share_token(user: User, document_id: int):
        try:
            document = document_service.get_document_check_access(document_id, user.id)
            if document.can_share:
                return jsonify({'data': document.share_token}), 201
            else:
                return jsonify({'error': 'Document is not shareable'}), 400
        except PDFDocument.DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except User.DoesNotExist:
            return jsonify({'error': 'User not found'}), 404
        except AuthorizationError as e:
            return jsonify({'error': str(e)}), 403
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    @document_bp.route('/<document_id>/share/<share_token>', methods=['POST'])
    @token_required
    def add_collaborator_via_token(user: User, document_id: int, share_token: str):
        try:
            document = document_service.get_document_check_access(document_id, user.id)
            user = user_service.get_user_by_id(user.id)

            if document.can_share and share_token == document.share_token:
                document_service.add_collaborator(user, document)
                return jsonify({'data': 'User added as collaborator'}), 201
            else:
                return jsonify({'error': 'Document is not shareable or token is incorrect'}), 400
        except PDFDocument.DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except User.DoesNotExist:
            return jsonify({'error': 'User not found'}), 404
        except AuthorizationError as e:
            return jsonify({'error': str(e)}), 403
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    return document_bp
