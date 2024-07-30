import logging
from typing import Dict, Any
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.app import db
from src.models import HighlightAnnotation
from src.schemas.annotation_schema import CreateAnnotationSchema, UpdateAnnotationSchema


class AnnotationService:
    @staticmethod
    def create_annotation(data: Dict[str, Any]):
        schema = CreateAnnotationSchema()
        try:
            validated_data = schema.load(data)
            annotation = HighlightAnnotation(**validated_data)
            db.session.add(annotation)
            db.session.commit()
            logging.debug("Created highlight annotation")
            return annotation
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            raise
        except SQLAlchemyError as err:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(err)}")
            raise

    @staticmethod
    def update_annotation(annotation: HighlightAnnotation, data: Dict[str, Any]):
        schema = UpdateAnnotationSchema()
        try:
            validated_data = schema.load(data)
            for key, value in validated_data.items():
                setattr(annotation, key, value)
            db.session.commit()
            logging.debug("Updated highlight annotation")
            return annotation
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            raise
        except SQLAlchemyError as err:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(err)}")
            raise

    @staticmethod
    def delete_annotation(annotation: HighlightAnnotation):
        try:
            db.session.delete(annotation)
            db.session.commit()
            logging.debug("Deleted highlight annotation")
        except SQLAlchemyError as err:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(err)}")
            raise

    @staticmethod
    def get_annotation_by_id(annotation_id: int) -> HighlightAnnotation:
        try:
            annotation = HighlightAnnotation.query.get(annotation_id)
            if not annotation:
                raise ValidationError("Annotation not found.")
            return annotation
        except SQLAlchemyError as e:
            logging.error("SQLAlchemy error: %s", str(e))
            raise
