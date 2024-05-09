from flask import jsonify, Blueprint
from mongoengine.errors import DoesNotExist

from services import user_service
from services import document_service


def create_user_bp():
    user_bp = Blueprint('user', __name__, url_prefix='/api/users')

    @user_bp.route('/<user_id>', methods=['GET'])
    def user_detail(user_id: int):
        try:
            user = user_service.get_user_by_id(user_id)
            return jsonify(user.to_mongo().to_dict()), 200
        except DoesNotExist:
            return jsonify({"error": "User not found"}), 404

    @user_bp.route('/<user_id>/documents', methods=['GET'])
    def get_documents(user_id: int):
        try:
            documents = document_service.get_documents_by_owner(user_id)
            return jsonify([doc.to_mongo().to_dict() for doc in documents]), 201
        except DoesNotExist:
            return jsonify({'error': 'Document not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return user_bp
