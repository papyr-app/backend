from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from mongoengine.errors import NotUniqueError, DoesNotExist

from auth.jwt_handler import generate_jwt
from services import user_service


def create_auth_bp(bcrypt: Bcrypt):
    auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

    @auth_bp.route('/register', methods=['POST'])
    def register():
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            user = user_service.create_user(data)
            return jsonify({'data': user.to_mongo().to_dict()}), 201
        except NotUniqueError as e:
            return jsonify({"error": str(e)}), 400

    @auth_bp.route('/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            user = user_service.get_user_by_username(username)
            if user.check_password(password):
                user.record_login()
                jwt = generate_jwt(str(user.id))
                return jsonify({'data': jwt}), 200
            else:
                return jsonify({'error': 'Invalid username or password'}), 401
        except DoesNotExist:
            return jsonify({'error': 'Invalid username or password'}), 401

    return auth_bp
