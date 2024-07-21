import logging
from flask_socketio import emit, join_room, leave_room
from marshmallow import ValidationError

from src.schemas.socket_schema import SocketSchema, MessageSchema


def handle_chat(socketio):
    @socketio.on("send_message")
    def handle_message(data):
        schema = MessageSchema()
        try:
            validated_data = schema.load(data)
            room = validated_data["room"]
            username = validated_data["username"]
            message = validated_data["message"]
            emit("new_message", {"username": username, "message": message}, room=room)
            logging.debug("%s sent a message: %s in room %s.", username, message, room)
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            emit("error", {"errors": err.messages})
        except Exception as err:
            logging.error("Error handling message: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"})

    @socketio.on("join")
    def on_join(data):
        schema = SocketSchema()
        try:
            validated_data = schema.load(data)
            room = validated_data["room"]
            username = validated_data["username"]
            join_room(room)
            emit(
                "new_message",
                {"username": "System", "message": f"{username} has joined the room."},
                room=room,
            )
            logging.debug("%s joined room %s.", username, room)
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            emit("error", {"errors": err.messages})
        except Exception as err:
            logging.error("Error joining room: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"})

    @socketio.on("leave")
    def on_leave(data):
        schema = SocketSchema()
        try:
            validated_data = schema.load(data)
            room = validated_data["room"]
            username = validated_data["username"]
            leave_room(room)
            emit(
                "new_message",
                {"username": "System", "message": f"{username} has joined the room."},
                room=room,
            )
            logging.debug("%s left room %s.", username, room)
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            emit("error", {"errors": err.messages})
        except Exception as err:
            logging.error("Error leaving room: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"})
