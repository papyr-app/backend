from flask import jsonify, Blueprint
from mongoengine.errors import DoesNotExist
from services import user_service


def create_user_bp():
    user_bp = Blueprint('user', __name__, url_prefix='/users')

    @user_bp.route('/<username>', methods=['GET'])
    def user_detail(username):
        try:
            user = user_service.get_user_by_username(username)
            return jsonify(user.to_mongo().to_dict()), 200
        except DoesNotExist:
            return jsonify({"error": "User not found"}), 404

    return user_bp
