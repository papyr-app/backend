import logging
from flask_socketio import emit
from marshmallow import ValidationError
from mongoengine.errors import DoesNotExist

from schemas.annotation_schema import CreateAnnotationSchema
from schemas.annotation_schema import UpdateAnnotationSchema
from services import annotation_service
from services import document_service
from services import user_service


def handle_annotations(socketio):
    @socketio.on("create_annotation")
    def handle_create_annotation(data):
        try:
            room = data["room_id"]
            payload = data["payload"]

            schema = CreateAnnotationSchema()
            validated_data = schema.load(payload)

            document = document_service.get_document(validated_data["document"])
            user = user_service.get_user_by_id(validated_data["user"])

            annotation_type = validated_data["annotation_type"]

            if annotation_type == "highlight":
                annotation = annotation_service.create_highlight_annotation(
                    document=document,
                    user=user,
                    page_number=validated_data["page_number"],
                    position=validated_data["position"],
                    layer=validated_data["layer"],
                    text_rage=validated_data["text_range"],
                    color=validated_data["color"],
                )
            elif annotation_type == "drawing":
                annotation = annotation_service.create_drawing_annotation(
                    document=document,
                    user=user,
                    page_number=validated_data["page_number"],
                    position=validated_data["position"],
                    layer=validated_data["layer"],
                    path=validated_data["path"],
                    color=validated_data["color"],
                    width=validated_data["width"],
                )
            else:
                raise ValueError("Unsupported annotation type")

            emit("new_annotation", annotation.to_json(), room=room, broadcast=True)
        except ValidationError as e:
            logging.exception(e)
            emit("annotation_error", {"error": str(e)})
        except DoesNotExist as e:
            logging.exception(e)
            emit("annotation_error", {"error": f"Invalid reference: {str(e)}"})
        except Exception as e:
            logging.exception(e)
            emit("annotation_error", {"error": "An error occurred"})

    @socketio.on("update_annotation")
    def handle_update_annotation(data):
        try:
            room = data["room_id"]
            payload = data["payload"]

            schema = UpdateAnnotationSchema()
            validated_data = schema.load(payload)

            annotation = annotation_service.get_annotation(validated_data["id"])
            annotation = annotation_service.update_annotation(
                annotation, validated_data
            )

            emit("updated_annotation", annotation.to_json(), room=room, broadcast=True)
        except ValidationError as e:
            emit("annotation_error", {"error": str(e)})
        except DoesNotExist as e:
            emit("annotation_error", {"error": f"Invalid reference: {str(e)}"})
        except Exception as e:
            logging.exception(e)
            emit("annotation_error", {"error": "An error occurred"})

    @socketio.on("delete_annotation")
    def handle_delete_annotation(data):
        try:
            room = data["room_id"]
            payload = data["payload"]

            annotation_id = payload.get("id")
            annotation_service.delete_annotation(annotation_id)

            emit("deleted_annotation", {"id": annotation_id}, room=room, broadcast=True)
        except DoesNotExist:
            emit("annotation_error", {"error": "Annotation not found"})
        except Exception as e:
            logging.exception(e)
            emit("annotation_error", {"error": "An error occurred"})
