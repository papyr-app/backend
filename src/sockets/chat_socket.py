import logging
from typing import Dict, Any
from flask_socketio import emit, join_room, leave_room
from marshmallow import ValidationError

from src.models import User
from src.auth.decorators import token_required_socket
from src.schemas.socket_schema import SocketSchema, MessageSchema


def handle_chat(socketio):
    @socketio.on("send_message")
    @token_required_socket
    def handle_message(user: User, data: Dict[str, Any]):
        schema = MessageSchema()
        try:
            validated_data = schema.load(data)
            room = validated_data["room"]
            message = validated_data["message"]
            emit("new_message", {"username": user.username, "message": message}, room=room)
            logging.debug("%s sent a message: %s in room %s.", user.username, message, room)
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            emit("error", {"errors": err.messages})
        except Exception as err:
            logging.error("Error handling message: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"})

    @socketio.on("join")
    @token_required_socket
    def on_join(user: User, data: Dict[str, Any]):
        schema = SocketSchema()
        try:
            validated_data = schema.load(data)
            room = validated_data["room"]
            join_room(room)
            emit(
                "new_message",
                {"username": "System", "message": f"{user.username} has joined the room."},
                room=room,
            )
            logging.debug("%s joined room %s.", user.username, room)
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            emit("error", {"errors": err.messages})
        except Exception as err:
            logging.error("Error joining room: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"})

    @socketio.on("leave")
    @token_required_socket
    def on_leave(user: User, data: Dict[str, Any]):
        schema = SocketSchema()
        try:
            validated_data = schema.load(data)
            room = validated_data["room"]
            leave_room(room)
            emit(
                "new_message",
                {"username": "System", "message": f"{user.username} has joined the room."},
                room=room,
            )
            logging.debug("%s left room %s.", user.username, room)
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            emit("error", {"errors": err.messages})
        except Exception as err:
            logging.error("Error leaving room: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"})
