import logging
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from marshmallow import ValidationError

from app import db
from errors import AuthorizationError
from services.pdf_document_service import PDFDocumentService
from schemas.invitation_schema import (
    InvitationSchema,
    CreateInvitationSchema,
    UpdateInvitationSchema,
    AcceptInvitationSchema,
)
from models.invitation import Invitation


class InvitationService:
    @staticmethod
    def create_invitation(data, user):
        schema = CreateInvitationSchema()
        try:
            validated_data = schema.load(data)
            invitee = validated_data["document_id"]
            document = PDFDocumentService.get_pdf_document_by_id(
                validated_data["document_id"]
            )

            if user != document.owner:
                raise ValidationError("User is already a collaborator")

            if user == invitee:
                raise ValidationError("User is already a collaborator")

            if invitee in document.collaborators:
                raise ValidationError("User is already a collaborator")

            invitation = Invitation(**validated_data)
            db.session.add(invitation)
            db.session.commit()
            return invitation
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def update_invitation(invitation_id, data):
        schema = UpdateInvitationSchema()
        try:
            invitation = Invitation.query.get(invitation_id)
            validated_data = schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(invitation, key, value)
            db.session.commit()
            return invitation
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def delete_invitation(invitation_id):
        try:
            invitation = Invitation.query.get(invitation_id)
            if not invitation:
                raise ValidationError("Invitation not found.")
            db.session.delete(invitation)
            db.session.commit()
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def get_invitation_by_id(invitation_id, user_id):
        try:
            invitation = Invitation.query.get(invitation_id)
            if not invitation:
                raise ValidationError("Invitation not found.")
            if not invitation.has_access(user_id):
                raise AuthorizationError()
            return invitation
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def get_invitations_sent_by_user(user_id):
        try:
            invitations = Invitation.query.filter_by(invited_by_id=user_id).all()
            return invitations
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def get_invitations_received_by_user(user_id):
        try:
            invitations = Invitation.query.filter_by(invitee_id=user_id).all()
            return invitations
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def accept_invitation(data, user):
        schema = AcceptInvitationSchema()
        try:
            validated_data = schema.load(data)
            invitation = InvitationService.get_invitation_by_id(
                validated_data["invitation_id"]
            )

            if invitation.invitee != user:
                raise ValidationError("Cannot invite yourself")

            if invitation.expires_at < datetime.utcnow():
                raise ValidationError("Invitation is expired")

            document_id = invitation.document_id
            invitee_id = invitation.invitee_id
            PDFDocumentService.add_collaborator(document_id, user.id, invitee_id)
            return invitation
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise
