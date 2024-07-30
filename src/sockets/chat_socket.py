import logging
from typing import Dict, Any
from flask_socketio import emit
from marshmallow import ValidationError

from src.models import User
from src.auth.decorators import token_required_socket
from src.schemas.socket_schema import MessageSchema


def handle_chat(socketio):
    @socketio.on("send_message")
    @token_required_socket
    def handle_message(user: User, room: str, data: Dict[str, Any]):
        schema = MessageSchema()
        try:
            validated_data = schema.load(data)
            message = validated_data["message"]
            emit(
                "new_message",
                {"username": user.username, "message": message},
                room=room,
                include_self=False,
            )
            logging.debug("%s #%s: '%s'", user.username, room, message)
            return
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            emit("error", {"errors": err.messages}, broadcast=False)
            return
        except Exception as err:
            logging.error("Error handling message: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"}, broadcast=False)
            return
