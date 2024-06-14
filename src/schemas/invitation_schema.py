from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields, validate, validates, ValidationError

from app import db
from models import Invitation, User, PDFDocument


class InvitationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Invitation
        include_fk = True
        load_instance = True
        sqla_session = db.session


class CreateInvitationSchema(Schema):
    document_id = fields.String(required=True, attribute="document_id")
    invitee = fields.String(
        required=True, validate=validate.Email(), attribute="invitee"
    )

    @validates("document_id")
    def validate_document(self, value):
        if not PDFDocument.query.get(value):
            raise ValidationError("Document not found.")

    @validates("invitee")
    def validate_invitee(self, value):
        if not User.query.filter_by(email=value).first():
            raise ValidationError("User with this email does not exist.")


class AcceptInvitationSchema(Schema):
    invitation_id = fields.String(required=True, attribute="invitation_id")

    @validates("invitation_id")
    def validate_invitation(self, value):
        if not Invitation.query.get(value):
            raise ValidationError("Invitation not found.")
