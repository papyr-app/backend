from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, validates, ValidationError

from models import Invitation, User, PDFDocument


class InvitationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Invitation
        include_fk = True
        load_instance = True


class CreateInvitationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Invitation
        load_instance = True
        include_fk = True

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


class AcceptInvitationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Invitation
        load_instance = True
        include_fk = True

    invitation_id = fields.String(required=True, attribute="id")

    @validates("invitation_id")
    def validate_invitation(self, value):
        if not Invitation.query.get(value):
            raise ValidationError("Invitation not found.")
