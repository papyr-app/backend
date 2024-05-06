from flask import jsonify, Blueprint
from services import user_service


user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/<username>', methods=['GET'])
def user_detail(username):
    user = user_service.get_user_by_username(username)
    if user:
        return jsonify(user.to_mongo().to_dict()), 200
    else:
        return jsonify({"error": "User not found"}), 404
