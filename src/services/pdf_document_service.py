import logging
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from marshmallow import ValidationError

from app import db
from errors import AuthorizationError
from services.user_service import UserService
from schemas.pdf_document_schema import (
    PDFDocumentSchema,
    CreatePDFDocumentSchema,
    UpdatePDFDocumentSchema,
)
from models.pdf_document import PDFDocument


class PDFDocumentService:
    @staticmethod
    def create_pdf_document(data):
        schema = CreatePDFDocumentSchema()
        try:
            validated_data = schema.load(data)
            pdf_document = PDFDocument(**validated_data)
            db.session.add(pdf_document)
            db.session.commit()
            return pdf_document
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def update_pdf_document(document_id, data, user_id):
        schema = UpdatePDFDocumentSchema()
        try:
            pdf_document = PDFDocumentService.get_pdf_document_by_id(
                document_id, user_id
            )
            validated_data = schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(pdf_document, key, value)
            db.session.commit()
            return pdf_document
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def delete_pdf_document(document_id):
        try:
            pdf_document = PDFDocument.query.get(document_id)
            if not pdf_document:
                raise ValidationError("PDF Document not found.")
            db.session.delete(pdf_document)
            db.session.commit()
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def get_pdf_document_by_id(document_id, user_id):
        try:
            pdf_document = PDFDocument.query.get(document_id)
            if not pdf_document:
                raise ValidationError("PDF Document not found.")
            if not pdf_document.has_access(user_id):
                raise AuthorizationError()
            return pdf_document
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def get_pdf_document_by_share_token(share_token, user_id):
        try:
            pdf_document = PDFDocument.query.filter(
                (PDFDocument.share_token == share_token)
            ).first()
            if not pdf_document:
                raise ValidationError("PDF Document not found.")
            return pdf_document
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def get_documents_by_user(user_id):
        try:
            pdf_documents = PDFDocument.query.filter(
                (PDFDocument.owner_id == user_id)
                | (PDFDocument.collaborators.any(id=user_id))
            ).all()
            return pdf_documents
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def add_collaborator(document_id, user_id, collaborator_id):
        try:
            pdf_document = PDFDocumentService.get_pdf_document_by_id(document_id)
            if not pdf_document:
                raise ValidationError("PDF Document not found.")

            collaborator = UserService.get_user_by_id(collaborator_id)
            if not collaborator:
                raise ValidationError("Collaborator not found.")

            if collaborator in pdf_document.collaborators:
                raise ValidationError("Collaborator is already added to the document.")

            pdf_document.collaborators.append(collaborator)
            db.session.commit()
            return pdf_document
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def remove_collaborator(document_id, user_id, collaborator_id):
        try:
            pdf_document = PDFDocumentService.get_pdf_document_by_id(document_id)
            if not pdf_document:
                raise ValidationError("PDF Document not found.")

            collaborator = UserService.get_user_by_id(collaborator_id)
            if not collaborator:
                raise ValidationError("Collaborator not found.")

            if collaborator not in pdf_document.collaborators:
                raise ValidationError(
                    "Collaborator is not associated with the document."
                )

            pdf_document.collaborators.remove(collaborator)
            db.session.commit()
            return pdf_document
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise
