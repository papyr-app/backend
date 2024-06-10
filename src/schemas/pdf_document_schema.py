from marshmallow import Schema, fields, validate, validates, ValidationError

from const import DocumentStatus


class CreatePDFDocumentSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=40))
    description = fields.String(required=False, validate=validate.Length(max=300))
    can_share = fields.Boolean(required=False, default=False)


class UpdatePDFDocumentSchema(Schema):
    title = fields.String(required=False, validate=validate.Length(min=1, max=40))
    description = fields.String(required=False, validate=validate.Length(max=300))
    status = fields.String(required=False)
    can_share = fields.Boolean(required=False)

    @validates("status")
    def validate_status(self, value):
        if value not in DocumentStatus.__members__:
            raise ValidationError("Invalid status.")
