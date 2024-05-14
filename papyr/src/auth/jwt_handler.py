import jwt
import datetime
from flask import current_app


def generate_jwt(user_id: str) -> str:
    payload = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'sub': user_id
    }
    secret_key = current_app.config['SECRET_KEY']
    return jwt.encode(payload, secret_key, algorithm='HS256')


def decode_jwt(token):
    try:
        secret_key = current_app.config['SECRET_KEY']
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
