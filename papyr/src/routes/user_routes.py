import logging
from flask import request, jsonify, Blueprint
from mongoengine.errors import DoesNotExist
from marshmallow import ValidationError

from auth.decorators import token_required
from services import user_service
from services import document_service
from schemas.user_schema import UpdateUserSchema


def create_user_bp():
    user_bp = Blueprint('user', __name__, url_prefix='/api/users')

    @user_bp.route('/<user_id>', methods=['GET'])
    @token_required
    def get_user(_, user_id: int):
        try:
            user = user_service.get_user_by_id(user_id)
            return jsonify({'data': user.to_mongo().to_dict()}), 200
        except DoesNotExist:
            return jsonify({"error": "User not found"}), 404
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    @user_bp.route('/<user_id>', methods=['PATCH'])
    @token_required
    def update_user(_, user_id: int):
        data = request.get_json()
        try:
            schema = UpdateUserSchema()
            validated_data = schema.load(data)
            user = user_service.get_user_by_id(user_id)
            user_service.update_user(user, validated_data)
            return jsonify({'data': user.to_mongo().to_dict()}), 200
        except DoesNotExist:
            return jsonify({"error": "User not found"}), 404
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    @user_bp.route('/<user_id>/documents', methods=['GET'])
    @token_required
    def get_documents(_, user_id: int):
        try:
            documents = document_service.get_documents_by_owner(user_id)
            return jsonify({'data': [doc.to_mongo().to_dict() for doc in documents]}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    @user_bp.route('/<user_id>/review_documents', methods=['GET'])
    @token_required
    def get_review_documents(_, user_id: int):
        try:
            documents = document_service.get_documents_by_collaborator(user_id)
            return jsonify({'data': [doc.to_mongo().to_dict() for doc in documents]}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    return user_bp
