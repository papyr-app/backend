from marshmallow import Schema, fields
from datetime import datetime, timedelta


class CreateInvitationSchema(Schema):
    document = fields.String(required=True)
    invited_by = fields.String(required=True)
    invitee = fields.String(required=True)
    expires_at = fields.DateTime(missing=lambda: datetime.utcnow() + timedelta(days=7))


class UpdateInvitationSchema(Schema):
    document = fields.String()
    invited_by = fields.String()
    invitee = fields.String()
    expires_at = fields.DateTime()
