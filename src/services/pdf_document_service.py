import logging
from typing import List, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from src.app import db
from src.errors import AuthorizationError
from src.schemas.pdf_document_schema import (
    CreatePDFDocumentSchema,
    UpdatePDFDocumentSchema,
)
from src.models import PDFDocument, VirtualPath, User


class PDFDocumentService:
    @staticmethod
    def create_pdf_document(data: Dict[str, Any], user_id: str) -> PDFDocument:
        schema = CreatePDFDocumentSchema()
        try:
            validated_data = schema.load(data)
            file_path = validated_data.pop("file_path")
            pdf_document = PDFDocument(**validated_data, owner_id=user_id)
            db.session.add(pdf_document)
            db.session.flush()

            virtual_path = VirtualPath(
                user_id=user_id, document_id=pdf_document.id, file_path=file_path
            )
            db.session.add(virtual_path)
            db.session.commit()
            logging.debug("Created document %s", pdf_document.id)
            return pdf_document
        except ValidationError as e:
            logging.error("Validation error: %s", e.messages)
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def update_pdf_document(
        pdf_document: PDFDocument, data: Dict[str, Any], user_id: str = None
    ) -> PDFDocument:
        schema = UpdatePDFDocumentSchema()
        try:
            validated_data = schema.load(data, partial=True)

            if "file_path" in validated_data and user_id:
                file_path = validated_data.pop("file_path")
                virtual_path = db.session.query(VirtualPath).filter_by(user_id=user_id, document_id=pdf_document.id).first()
                if virtual_path:
                    virtual_path.file_path = file_path
                else:
                    virtual_path = VirtualPath(
                        user_id=user_id,
                        document_id=pdf_document.id,
                        file_path=file_path,
                    )
                    db.session.add(virtual_path)

            for key, value in validated_data.items():
                setattr(pdf_document, key, value)

            db.session.commit()
            logging.debug("Updated document %s", pdf_document.id)
            return pdf_document
        except ValidationError as e:
            logging.error("Validation error: %s", e.messages)
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error("SQLAlchemy error: %s", str(e))
            raise

    @staticmethod
    def delete_pdf_document(pdf_document: PDFDocument) -> None:
        try:
            db.session.delete(pdf_document)
            db.session.commit()
            logging.debug("Deleted document %s", pdf_document.id)
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error("SQLAlchemy error: %s", str(e))
            raise

    @staticmethod
    def get_pdf_document_by_id(document_id: str) -> PDFDocument:
        try:
            pdf_document = db.session.get(PDFDocument, document_id)
            if not pdf_document:
                raise ValidationError("PDF Document not found.")
            return pdf_document
        except SQLAlchemyError as e:
            logging.error("SQLAlchemy error: %s", str(e))
            raise

    @staticmethod
    def get_pdf_document_by_share_token(share_token: str) -> PDFDocument:
        try:
            pdf_document = PDFDocument.query.filter(
                (PDFDocument.share_token == share_token)
            ).first()
            if not pdf_document:
                raise ValidationError("PDF Document not found.")
            return pdf_document
        except SQLAlchemyError as e:
            logging.error("SQLAlchemy error: %s", str(e))
            raise

    @staticmethod
    def get_documents_by_user(user_id: str) -> List[PDFDocument]:
        try:
            pdf_documents = PDFDocument.query.filter(
                (PDFDocument.owner_id == user_id)
                | (PDFDocument.collaborators.any(id=user_id))
            ).all()
            return pdf_documents
        except SQLAlchemyError as e:
            logging.error("SQLAlchemy error: %s", str(e))
            raise

    @staticmethod
    def add_collaborator(pdf_document: PDFDocument, collaborator: User) -> PDFDocument:
        try:
            if collaborator in pdf_document.collaborators:
                raise ValidationError("User is already a collaborator.")

            if collaborator == pdf_document.owner:
                raise ValidationError("User owns the document.")

            pdf_document.collaborators.append(collaborator)
            db.session.flush()

            virtual_path = VirtualPath(
                user_id=collaborator.id, document_id=pdf_document.id
            )
            db.session.add(virtual_path)
            db.session.commit()
            logging.debug(
                "Added collaborator %s to document %s", collaborator.id, pdf_document.id
            )
            return pdf_document
        except ValidationError as e:
            logging.error("Validation error: %s", e.messages)
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error("SQLAlchemy error: %s", str(e))
            raise

    @staticmethod
    def remove_collaborator(
        pdf_document: PDFDocument, collaborator: User
    ) -> PDFDocument:
        try:
            if collaborator not in pdf_document.collaborators:
                raise ValidationError("User is not associated with the document.")

            virtual_path = db.session.query(VirtualPath).filter_by(user_id=collaborator.id, document_id=pdf_document.id).first()
            if virtual_path:
                db.session.delete(virtual_path)

            pdf_document.collaborators.remove(collaborator)
            db.session.commit()
            logging.debug(
                "Removed collaborator %s from document %s",
                collaborator.id,
                pdf_document.id,
            )
            return pdf_document
        except ValidationError as e:
            logging.error("Validation error: %s", e.messages)
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error("SQLAlchemy error: %s", str(e))
            raise

    @staticmethod
    def check_user_access(document: PDFDocument, user_id: str) -> bool:
        if not document.has_access(user_id):
            raise AuthorizationError()
        return True
