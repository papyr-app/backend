import logging
from typing import Dict, Any
from flask_socketio import emit
from marshmallow import ValidationError

from src.auth.decorators import token_required_socket
from src.services.annotation_service import AnnotationService
from src.schemas.annotation_schema import AnnotationSchema
from src.models import User


def handle_annotations(socketio):
    @socketio.on("get_annotations")
    @token_required_socket
    def handle_get_annotations(user: User, room: str, data: Dict[str, Any]):
        pass

    @socketio.on("create_annotation")
    @token_required_socket
    def handle_create_annotation(user: User, room: str, data: Dict[str, Any]):
        try:
            annotation = AnnotationService.create_annotation(data, user.id)
            emit("new_annotation", AnnotationSchema().dump(annotation), room=room)
            return
        except ValidationError as err:
            emit("error", {"errors": err.messages}, broadcast=False)
            return
        except Exception as err:
            logging.error("Error creating annotation: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"}, broadcast=False)
            return

    @socketio.on("update_annotation")
    @token_required_socket
    def handle_update_annotation(_, room: str, data: Dict[str, Any]):
        annotation_id = data.pop("annotation_id", None)
        if not annotation_id:
            emit("error", {"errors": "Missing annotation ID"}, broadcast=False)
            return

        try:
            annotation = AnnotationService.get_annotation_by_id(annotation_id)
            annotation = AnnotationService.update_annotation(annotation, data)
            emit("updated_annotation", AnnotationSchema().dump(annotation), room=room)
        except ValidationError as err:
            emit("error", {"errors": err.messages}, broadcast=False)
            return
        except Exception as err:
            logging.error("Error creating annotation: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"}, broadcast=False)
            return

    @socketio.on("delete_annotation")
    @token_required_socket
    def handle_delete_annotation(_, room: str, data: Dict[str, Any]):
        annotation_id = data.pop("annotation_id", None)
        if not annotation_id:
            emit("error", {"errors": "Missing annotation ID"}, broadcast=False)
            return

        try:
            annotation = AnnotationService.get_annotation_by_id(annotation_id)
            annotation = AnnotationService.delete_annotation(annotation)
            emit("deleted_annotation", AnnotationSchema().dump(annotation), room=room)
        except ValidationError as err:
            emit("error", {"errors": err.messages}, broadcast=False)
            return
        except Exception as err:
            logging.error("Error creating annotation: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"}, broadcast=False)
            return
