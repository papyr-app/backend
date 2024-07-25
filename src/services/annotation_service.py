import logging
from typing import Dict, Any
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.app import db
from src.models import HighlightAnnotation, User
from src.schemas.annotation_schema import CreateAnnotationSchema, UpdateAnnotationSchema


class AnnotationService:
    @staticmethod
    def create_annotation(data: Dict[str, Any], user: User):
        schema = CreateAnnotationSchema()
        try:
            validated_data = schema.load(data)
            annotation = HighlightAnnotation(**validated_data)
            db.session.add(annotation)
            db.session.commit()
            logging.debug('Created highlight annotation')
            return annotation
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            raise
        except SQLAlchemyError as err:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(err)}")
            raise

    @staticmethod
    def update_annotation(data: Dict[str, Any]):
        pass

    @staticmethod
    def delete_annotation(data: Dict[str, Any]):
        pass
