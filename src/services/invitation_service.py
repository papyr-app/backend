import logging
from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from src.errors import AuthorizationError
from src.app import db
from src.models import User, Invitation
from src.services.pdf_document_service import PDFDocumentService
from src.services.user_service import UserService
from src.schemas.invitation_schema import (
    CreateInvitationSchema,
    AcceptInvitationSchema,
)


class InvitationService:
    @staticmethod
    def create_invitation(data: Dict[str, Any], user: User) -> Invitation:
        schema = CreateInvitationSchema()
        try:
            validated_data = schema.load(data)
            invitee = UserService.get_user_by_email(validated_data["invitee"])
            document = PDFDocumentService.get_pdf_document_by_id(
                validated_data["document_id"]
            )

            if user == invitee:
                raise ValidationError("Cannot invite yourself.")

            if invitee == document.owner or invitee in document.collaborators:
                raise ValidationError("User is already a collaborator.")

            invitation = Invitation(
                document_id=document.id, invited_by_id=user.id, invitee_id=invitee.id
            )
            db.session.add(invitation)
            db.session.commit()
            logging.debug("Created invitation %s", invitation.id)
            return invitation
        except ValidationError as e:
            logging.error("Validation error %s", e.messages)
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error("SQLAlchemy error: %s", str(e))
            raise

    @staticmethod
    def get_invitation_by_id(invitation_id: str) -> Invitation:
        try:
            invitation = Invitation.query.get(invitation_id)
            if not invitation:
                raise ValidationError("Invitation not found.")
            return invitation
        except SQLAlchemyError as e:
            logging.error("SQLAlchemy error: %s", str(e))
            raise

    @staticmethod
    def get_invitations_sent_by_user(user_id: str) -> List[Invitation]:
        try:
            invitations = Invitation.query.filter_by(invited_by_id=user_id).all()
            return invitations
        except SQLAlchemyError as e:
            logging.error("SQLAlchemy error: %s", str(e))
            raise

    @staticmethod
    def get_invitations_received_by_user(user_id: str) -> List[Invitation]:
        try:
            invitations = Invitation.query.filter_by(invitee_id=user_id).all()
            return invitations
        except SQLAlchemyError as e:
            logging.error("SQLAlchemy error: %s", str(e))
            raise

    @staticmethod
    def accept_invitation(data: Dict[str, Any], user: User) -> Invitation:
        schema = AcceptInvitationSchema()
        try:
            validated_data = schema.load(data)
            invitation = InvitationService.get_invitation_by_id(
                validated_data["invitation_id"]
            )

            if invitation.invitee != user:
                raise ValidationError("This is not your invite.")

            if invitation.expires_at < datetime.utcnow():
                raise ValidationError("Invitation is expired")

            document = PDFDocumentService.get_pdf_document_by_id(invitation.document_id)
            PDFDocumentService.add_collaborator(document, user)
            return invitation
        except ValidationError as e:
            logging.error("Validation error: %s", e.messages)
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error("SQLAlchemy error: %s", str(e))
            raise

    @staticmethod
    def check_user_access(invitation: Invitation, user_id: str) -> bool:
        if not invitation.has_access(user_id):
            raise AuthorizationError()
        return True
