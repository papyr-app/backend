from flask import jsonify, Blueprint
from services import user_service


user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/<username>', methods=['GET'])
def user_detail(username):
    user = user_service.get_user_by_username(username)
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


@user_bp.route('', methods=['GET'])
def users():
    pass
