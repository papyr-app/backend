import logging
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from app import db
from models.annotation import Annotation, DrawingAnnotation, HighlightAnnotation
from schemas.annotation_schema import (
    CreateDrawingAnnotationSchema,
    UpdateDrawingAnnotationSchema,
    CreateHighlightAnnotationSchema,
    UpdateHighlightAnnotationSchema,
)


class AnnotationService:
    @staticmethod
    def create_drawing_annotation(data):
        schema = CreateDrawingAnnotationSchema()
        try:
            validated_data = schema.load(data)
            annotation = DrawingAnnotation(**validated_data)
            db.session.add(annotation)
            db.session.commit()
            return annotation
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def create_highlight_annotation(data):
        schema = CreateHighlightAnnotationSchema()
        try:
            validated_data = schema.load(data)
            annotation = HighlightAnnotation(**validated_data)
            db.session.add(annotation)
            db.session.commit()
            return annotation
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def update_annotation(annotation_id, data):
        try:
            annotation = Annotation.query.get(annotation_id)
            if not annotation:
                raise ValidationError("Annotation not found.")

            if isinstance(annotation, DrawingAnnotation):
                schema = UpdateDrawingAnnotationSchema()
            elif isinstance(annotation, HighlightAnnotation):
                schema = UpdateHighlightAnnotationSchema()
            else:
                raise ValidationError("Invalid annotation type.")

            validated_data = schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(annotation, key, value)
            db.session.commit()
            return annotation
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def delete_annotation(annotation_id):
        try:
            annotation = Annotation.query.get(annotation_id)
            if not annotation:
                raise ValidationError("Annotation not found.")
            db.session.delete(annotation)
            db.session.commit()
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise
