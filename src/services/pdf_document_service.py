import logging
from typing import List, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from marshmallow import ValidationError

from app import db
from errors import AuthorizationError
from services.user_service import UserService
from schemas.pdf_document_schema import (
    CreatePDFDocumentSchema,
    UpdatePDFDocumentSchema,
)
from models import PDFDocument, VirtualPath, User


class PDFDocumentService:
    @staticmethod
    def create_pdf_document(data: Dict[str, Any], user_id: int) -> PDFDocument:
        schema = CreatePDFDocumentSchema()
        try:
            validated_data = schema.load(data)
            file_path = validated_data.pop("file_path")
            pdf_document = PDFDocument(**validated_data, owner_id=user_id)
            db.session.add(pdf_document)
            db.session.flush()

            virtual_path = VirtualPath(user_id=user_id, document_id=pdf_document.id, file_path=file_path)
            db.session.add(virtual_path)
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
    def update_pdf_document(
        document_id: int, data: Dict[str, Any], user_id: int
    ) -> PDFDocument:
        schema = UpdatePDFDocumentSchema()
        try:
            pdf_document = PDFDocumentService.get_pdf_document_by_id(document_id)
            validated_data = schema.load(data, partial=True)
            PDFDocumentService.check_user_access(pdf_document, user_id)

            if "file_path" in validated_data:
                file_path = validated_data.pop("file_path")
                virtual_path = VirtualPath.query.filter_by(user_id=user_id, document_id=document_id).first()
                if virtual_path:
                    virtual_path.file_path = file_path
                else:
                    virtual_path = VirtualPath(user_id=user_id, document_id=document_id, file_path=file_path)
                    db.session.add(virtual_path)

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
    def delete_pdf_document(document_id: int, user_id: int) -> None:
        try:
            pdf_document = PDFDocumentService.get_pdf_document_by_id(document_id)
            PDFDocumentService.check_user_access(pdf_document, user_id)
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
    def get_pdf_document_by_id(document_id: int) -> PDFDocument:
        try:
            pdf_document = PDFDocument.query.get(document_id)
            if not pdf_document:
                raise ValidationError("PDF Document not found.")
            return pdf_document
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def get_pdf_document_by_share_token(share_token: str) -> PDFDocument:
        try:
            pdf_document = PDFDocument.query.filter((PDFDocument.share_token == share_token)).first()
            if not pdf_document:
                raise ValidationError("PDF Document not found.")
            return pdf_document
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def get_documents_by_user(user_id: int) -> List[PDFDocument]:
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
    def add_collaborator(pdf_document: PDFDocument, collaborator: User) -> PDFDocument:
        try:
            if collaborator in pdf_document.collaborators:
                raise ValidationError("Collaborator is already added to the document.")

            pdf_document.collaborators.append(collaborator)
            db.session.flush()

            virtual_path = VirtualPath(user_id=collaborator.id, document_id=pdf_document.id)
            db.session.add(virtual_path)
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
    def remove_collaborator(pdf_document: PDFDocument, collaborator: User) -> PDFDocument:
        try:
            if collaborator not in pdf_document.collaborators:
                raise ValidationError("Collaborator is not associated with the document.")

            virtual_path = VirtualPath.query.filter_by(user_id=collaborator.id, document_id=pdf_document.id).first()
            if virtual_path:
                db.session.delete(virtual_path)

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

    @staticmethod
    def check_user_access(document: PDFDocument, user_id: int) -> bool:
        if not document.has_access(user_id):
            raise AuthorizationError()
        return True
