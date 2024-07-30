import datetime
from typing import Dict, Any
import jwt
from flask import current_app


def generate_jwt(payload: Dict[str, Any]) -> str:
    payload.update(
        {
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        }
    )
    secret_key = current_app.config["SECRET_KEY"]
    return jwt.encode(payload, secret_key, algorithm="HS256")


def decode_jwt(token: str) -> Dict[str, Any]:
    try:
        secret_key = current_app.config["SECRET_KEY"]
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
