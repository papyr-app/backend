from flask import jsonify, Blueprint
from src.services.user_service import get_user


user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/<username>', methods=['GET'])
def user_detail(username):
    user = get_user(username)
    if user:
        user_info = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role
        }
        return jsonify(user_info), 200
    else:
        return jsonify({"error": "User not found"}), 404
