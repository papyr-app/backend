import logging
from flask import request, jsonify, Blueprint
from mongoengine.errors import DoesNotExist

from auth.decorators import token_required
from services import virtual_path_service
from models.user import User


def create_virtual_path_bp():
    virtual_path_bp = Blueprint('virtual_path', __name__, url_prefix='/api/virtual_path')

    @virtual_path_bp.route('/<virtual_path_id>', methods=['PATCH'])
    @token_required
    def update_virtual_path(user: User, virtual_path_id: str):
        data = request.json
        try:
            virtual_path = virtual_path_service.get_user_virtual_path(virtual_path_id)
            virtual_path = virtual_path_service.update_virtual_path(virtual_path, data)
            return jsonify({'data': virtual_path.to_mongo().to_dict()}), 200
        except DoesNotExist:
            return jsonify({"error": "Virtual path does not exist"}), 404
        except Exception as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 500

    return virtual_path_bp
