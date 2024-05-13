from flask import request, jsonify, Blueprint
from mongoengine.errors import ValidationError, DoesNotExist, NotUniqueError

from services import document_service
from services import user_service
from models.user import User
from models.pdf_document import PDFDocument


def create_document_bp():
    document_bp = Blueprint('document', __name__, url_prefix='/api/documents')

    @document_bp.route('/<document_id>', methods=['GET'])
    def get_document(document_id: int):
        try:
            document = document_service.get_document(document_id)
            return jsonify(document.to_mongo().to_dict()), 201
        except DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @document_bp.route('/', methods=['POST'])
    def create_document():
        data = request.get_json()

        # TODO - instead of owner id grab user id from JWT
        owner = data.get('owner')
        file_path = data.get('file_path')
        title = data.get('title')

        if not owner or not file_path or not title:
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            document = document_service.create_document(data)
            return jsonify(document.to_mongo().to_dict()), 201
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except NotUniqueError:
            return jsonify({'error': 'Document already exists'}), 409
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @document_bp.route('/<document_id>', methods=['PATCH'])
    def update_document(document_id: int):
        data = request.get_json()

        # TODO - check if user has permissions to update this document

        try:
            document = document_service.get_document(document_id)
        except DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        try:
            updated_document = document_service.update_document(document, data)
            return jsonify(updated_document.to_mongo().to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @document_bp.route('/<document_id>', methods=['DELETE'])
    def delete_document(document_id):
        # TODO - check if user has permissions to delete this document
        try:
            document_service.delete_document(document_id)
            return jsonify({'message': 'Document deleted successfully'}), 200
        except DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @document_bp.route('/<document_id>/add_collaborator', methods=['POST'])
    def add_collaborator(document_id: int):
        data = request.get_json()
        email = data.get('email')

        # TODO - check if user has permissions to add collaborators

        if not email:
            return jsonify({'error': 'Missing required field'}), 404

        try:
            document = document_service.get_document(document_id)
            user = user_service.get_user_by_email(email)
            document_service.add_collaborator(user, document)
            return jsonify({'message': 'Collaborator added'}), 200
        except PDFDocument.DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except User.DoesNotExist:
            return jsonify({'error': 'User not found'}), 404

    @document_bp.route('/<document_id>/remove_collaborator', methods=['POST'])
    def remove_collaborator(document_id: int):
        data = request.get_json()
        email = data.get('email')

        # TODO - check if user has permissions to remove collaborators

        if not email:
            return jsonify({'error': 'Missing required field'}), 404

        try:
            document = document_service.get_document(document_id)
            user = user_service.get_user_by_email(email)
            document_service.remove_collaborator(user, document)
            return jsonify({'message': 'Collaborator removed'}), 200
        except PDFDocument.DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except User.DoesNotExist:
            return jsonify({'error': 'User not found'}), 404

    return document_bp
