import logging
from typing import Dict, Any
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.app import db
from src.models import HighlightAnnotation, User
from src.services.pdf_document_service import PDFDocumentService
from src.schemas.annotation_schema import CreateAnnotationSchema, UpdateAnnotationSchema


class AnnotationService:
    @staticmethod
    def create_annotation(data: Dict[str, Any], user: User):
        schema = CreateAnnotationSchema()
        try:
            validated_data = schema.load(data)
            pdf_document = PDFDocumentService.get_pdf_document_by_id(validated_data['document_id'])
            PDFDocumentService.check_user_access(pdf_document, user.id)
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
    def update_annotation(annotation_id: int, data: Dict[str, Any], user: User):
        schema = UpdateAnnotationSchema()
        try:
            annotation = 
            validated_data = schema.load(data)
            pdf_document = PDFDocumentService.get_pdf_document_by_id(validated_data['document_id'])
            PDFDocumentService.check_user_access(pdf_document, user.id)

            for key, value in validated_data.items():
                setattr(, key, value)

            db.session.commit()
            logging.debug("Created highlight annotation")
            return 
        except ValidationError as err:
            logging.error("Validation error: %s", err.messages)
            raise
        except SQLAlchemyError as err:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(err)}")
            raise

    @staticmethod
    def delete_annotation(data: Dict[str, Any], user: User):
        schema = CreateAnnotationSchema()
        try:
            validated_data = schema.load(data)
            pdf_document = PDFDocumentService.get_pdf_document_by_id(validated_data['document_id'])
            PDFDocumentService.check_user_access(pdf_document, user.id)
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
