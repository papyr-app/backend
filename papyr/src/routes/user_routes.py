import logging
from flask import request, jsonify, Blueprint
from mongoengine.errors import DoesNotExist
from marshmallow import ValidationError

from auth.decorators import token_required
from services import user_service
from services import document_service
from services import virtual_path_service
from schemas.user_schema import UpdateUserSchema
from models.user import User


def create_user_bp():
    user_bp = Blueprint('user', __name__, url_prefix='/api/users')

    @user_bp.route('', methods=['GET'])
    @token_required
    def get_user(user: User):
        try:
            user = user_service.get_user_by_id(user.id)
            return jsonify({'data': user.to_mongo().to_dict()}), 200
        except DoesNotExist:
            return jsonify({"error": "User not found"}), 404
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    @user_bp.route('', methods=['PATCH'])
    @token_required
    def update_user(user: User):
        data = request.get_json()
        try:
            schema = UpdateUserSchema()
            validated_data = schema.load(data)
            user = user_service.get_user_by_id(user.id)
            user_service.update_user(user, validated_data)
            return jsonify({'data': user.to_mongo().to_dict()}), 200
        except DoesNotExist:
            return jsonify({"error": "User not found"}), 404
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    @user_bp.route('/documents', methods=['GET'])
    @token_required
    def get_documents(user: User):
        try:
            documents = document_service.get_user_documents(user.id)

            # If the user is a collaborator, replace the path with their own
            for document in documents:
                if document.owner != user:
                    # If they don't have their own path, just use username
                    virtual_path = virtual_path_service.get_user_virtual_path(user.id, document.id)
                    document.file_path = virtual_path or user.username

            return jsonify({'data': [doc.to_mongo().to_dict() for doc in documents]}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    return user_bp
