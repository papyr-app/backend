import logging
from typing import Dict, Any
from flask_socketio import emit, join_room, leave_room
from marshmallow import ValidationError

from src.models import User
from src.services.pdf_document_service import PDFDocumentService
from src.auth.decorators import token_required_socket
from src.schemas.socket_schema import RoomSchema


def handle_connections(socketio):
    @socketio.on("connect")
    def handle_connect():
        logging.debug("User connected to Socket.")

    @socketio.on("disconnect")
    def handle_disconnect():
        logging.debug("User disconnected from Socket.")

    @socketio.on("join")
    @token_required_socket
    def on_join(user: User, data: Dict[str, Any]):
        schema = RoomSchema()
        try:
            validated_data = schema.load(data)
            room = validated_data["room"]

            pdf_document = PDFDocumentService.get_pdf_document_by_id(room)
            PDFDocumentService.check_user_access(pdf_document, user.id)

            join_room(room)
            emit(
                "new_message",
                {
                    "username": "System",
                    "message": f"{user.username} has joined the room.",
                },
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
        schema = RoomSchema()
        try:
            validated_data = schema.load(data)
            room = validated_data["room"]
            leave_room(room)
            emit(
                "new_message",
                {
                    "username": "System",
                    "message": f"{user.username} has left the room.",
                },
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
