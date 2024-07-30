import logging
from typing import Dict, Any
from flask_socketio import emit
from marshmallow import ValidationError

from src.errors import AuthorizationError
from src.auth.decorators import token_required_socket
from src.services.annotation_service import AnnotationService
from src.schemas.annotation_schema import AnnotationSchema
from src.models import User


def handle_annotations(socketio):
    @socketio.on("create_annotation")
    @token_required_socket
    def handle_create_annotation(user: User, data: Dict[str, Any]):
        try:
            annotation = AnnotationService.create_annotation(data, user)
            emit("new_annotation", AnnotationSchema().dump(annotation))
        except AuthorizationError as err:
            emit("error", {"errors": err.messages})
        except ValidationError as err:
            emit("error", {"errors": err.messages})
        except Exception as err:
            logging.error("Error creating annotation: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"})

    @socketio.on("update_annotation")
    @token_required_socket
    def handle_update_annotation(user: User, data: Dict[str, Any]):
        try:
            annotation = AnnotationService.update_annotation(data, user)
            emit("updated_annotation", AnnotationSchema().dump(annotation))
        except AuthorizationError as err:
            emit("error", {"errors": err.messages})
        except ValidationError as err:
            emit("error", {"errors": err.messages})
        except Exception as err:
            logging.error("Error creating annotation: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"})

    @socketio.on("delete_annotation")
    @token_required_socket
    def handle_delete_annotation(user: User, data: Dict[str, Any]):
        try:
            annotation = AnnotationService.delete_annotation(data, user)
            emit("deleted_annotation", AnnotationSchema().dump(annotation))
        except AuthorizationError as err:
            emit("error", {"errors": err.messages})
        except ValidationError as err:
            emit("error", {"errors": err.messages})
        except Exception as err:
            logging.error("Error creating annotation: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"})
