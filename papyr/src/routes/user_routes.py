from flask import request, jsonify, Blueprint

from services import user_service


user_bp = Blueprint('user_route', __name__, url_prefix='/api/user', template_folder='templates')


@user_bp.route('', methods=['POST'])
def create_user():
    user_data = request.json
    if 'email' not in user_data or 'password' not in user_data:
        return jsonify({"error": "Missing data"}), 400

    try:
        user = user_service.create_user(user_data)
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
