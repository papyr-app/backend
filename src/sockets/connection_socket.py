import logging
from flask_socketio import emit, join_room, leave_room, disconnect
from marshmallow import ValidationError

from src.models import User
from src.services.pdf_document_service import PDFDocumentService
from src.auth.decorators import token_required_socket


def handle_connections(socketio):
    @socketio.on("connect")
    @token_required_socket
    def handle_connect(user: User, room: str):
        logging.debug("User connected to Socket.")
        handle_join_room(user, room)

    @socketio.on("disconnect")
    @token_required_socket
    def handle_disconnect(user: User, room: str):
        logging.debug("User disconnected from Socket.")
        handle_leave_room(user, room)

    def handle_join_room(user: User, room: str):
        try:
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
                include_self=False
            )
            logging.debug("%s joined room %s.", user.username, room)
            return
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            emit("error", {"errors": err.messages}, broadcast=False)
            disconnect()
            return
        except Exception as err:
            logging.error("Error joining room: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"}, broadcast=False)
            disconnect()
            return

    def handle_leave_room(user: User, room: str):
        try:
            leave_room(room)
            emit(
                "new_message",
                {
                    "username": "System",
                    "message": f"{user.username} has left the room.",
                },
                room=room,
                include_self=False
            )
            logging.debug("%s left room %s.", user.username, room)
            return
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            emit("error", {"errors": err.messages}, broadcast=False)
            disconnect()
            return
        except Exception as err:
            logging.error("Error leaving room: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"}, broadcast=False)
            disconnect()
            return
