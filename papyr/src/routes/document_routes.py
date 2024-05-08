from datetime import datetime
from flask import request, jsonify, Blueprint
from mongoengine.errors import ValidationError, DoesNotExist, NotUniqueError

from services import document_service
from services import user_service
from services import invitation_service
from models.user import User
from models.document import PDFDocument
from models.invitation import Invitation


def create_document_bp():
    document_bp = Blueprint('document', __name__, '/documents')

    @document_bp.route('/<document_id>', methods=['GET'])
    def get_document(document_id: int):
        try:
            document = document_service.get_document(document_id)
            return jsonify(document.to_mongo().to_dict()), 201
        except DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @document_bp.route('/<user_id>', methods=['GET'])
    def get_documents(user_id: int):
        try:
            documents = document_service.get_documents(user_id)
            return jsonify([doc.to_mongo().to_dict() for doc in documents]), 201
        except DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @document_bp.route('', methods=['POST'])
    def create_document():
        data = request.get_json()

        owner_id = data.get('owner_id')
        file_path = data.get('file_path')
        title = data.get('title')

        if not owner_id or not file_path or not title:
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

    @document_bp.route('/<document_id>', methods=['UPDATE'])
    def update_document(document_id: int):
        data = request.get_json()

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

    @document_bp.route('/<document_id>/add_collaborator', methods=['POST'])
    def remove_collaborator(document_id: int):
        data = request.get_json()

        email = data.get('email')

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

    @document_bp.route('/<document_id>/invite', methods=['POST'])
    def create_invitation(document_id):
        data = request.get_json()

        email = data.get('email', None)

        if not email:
            return jsonify({'error': 'Missing required fields'})

        try:
            user = user_service.get_user_by_email(email)
            document = document_service.get_document(document_id)
            invitation = invitation_service.create_invitation(user, document)
            return jsonify(invitation.to_mongo().to_dict()), 200
        except Invitation.DoesNotExist:
            return jsonify({'error': 'Invitation does not exist'}), 400
        except User.DoesNotExist:
            return jsonify({'error': 'User does not exist'}), 400

    @document_bp.route('/<document_id>/invite/<invite_id>', methods=['POST'])
    def handle_invitation(document_id, invite_id):
        data = request.get_json()

        email = data.get('email', None)

        if not email:
            return jsonify({'error': 'Missing required fields'})

        try:
            invitation = invitation_service.get_invitation(invite_id)
            if invitation.expires_at < datetime.now():
                return jsonify({'error': 'Invitation is expired'}), 400

            user = user_service.get_user_by_email(email)
            document_service.add_collaborator(user, invitation.document)

            return "You have been granted access to the document.", 200
        except Invitation.DoesNotExist:
            return jsonify({'error': 'Invitation does not exist'}), 400
        except User.DoesNotExist:
            return jsonify({'error': 'User does not exist'}), 400

    return document_bp
