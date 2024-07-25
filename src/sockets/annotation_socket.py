import logging
from typing import Dict, Any
from flask_socketio import emit
from marshmallow import ValidationError

from src.errors import AuthorizationError
from src.services.annotation_service import AnnotationService
from src.services.pdf_document_service import PDFDocumentService
from src.schemas.annotation_schema import AnnotationSchema


def handle_annotations(socketio):
    @socketio.on("create_annotation")
    def handle_create_annotation(data: Dict[str, Any]):
        try:
            annotation = AnnotationService.create_annotation(data)
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
    def handle_update_annotation(data: Dict[str, Any]):
        try:
            annotation = AnnotationService.update_annotation(data)
            emit("new_annotation", AnnotationSchema().dump(annotation))
        except AuthorizationError as err:
            emit("error", {"errors": err.messages})
        except ValidationError as err:
            emit("error", {"errors": err.messages})
        except Exception as err:
            logging.error("Error creating annotation: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"})

    @socketio.on("delete_annotation")
    def handle_delete_annotation(data: Dict[str, Any]):
        try:
            annotation = AnnotationService.delete_annotation(data)
            emit("new_annotation", AnnotationSchema().dump(annotation))
        except AuthorizationError as err:
            emit("error", {"errors": err.messages})
        except ValidationError as err:
            emit("error", {"errors": err.messages})
        except Exception as err:
            logging.error("Error creating annotation: %s", str(err))
            logging.error("Exception", exc_info=True)
            emit("error", {"errors": "Internal error"})
