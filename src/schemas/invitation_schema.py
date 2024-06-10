from marshmallow import Schema, fields, validate, validates, ValidationError

from models.invitation import Invitation
from models.user import User
from models.pdf_document import PDFDocument


class CreateInvitationSchema(Schema):
    document = fields.String(required=True)
    invitee = fields.String(required=True, validate=validate.Email())

    @validates("document")
    def validate_document(self, value):
        if not PDFDocument.objects(id=value).first():
            raise ValidationError("Document not found.")

    @validates("invitee")
    def validate_invitee(self, value):
        if not User.objects(email=value).first():
            raise ValidationError("User with this email does not exist.")


class AcceptInvitationSchema(Schema):
    invitation = fields.String(required=True)

    @validates("invitation")
    def validate_document(self, value):
        if not Invitation.objects(id=value).first():
            raise ValidationError("Invitation not found.")
