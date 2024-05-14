from marshmallow import Schema, fields, validate, validates, ValidationError

from const import DocumentStatus


class CreatePDFDocumentSchema(Schema):
    owner = fields.String(required=True)
    file_path = fields.String(required=True, validate=validate.Length(min=1))
    title = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(missing=None)
    status = fields.String(missing=DocumentStatus.ACTIVE)
    collaborators = fields.List(fields.String(), missing=[])
    can_share = fields.Boolean(missing=False)
    share_token = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UpdatePDFDocumentSchema(Schema):
    file_path = fields.String(validate=validate.Length(min=1))
    title = fields.String(validate=validate.Length(min=1))
    description = fields.String()
    status = fields.String()
    collaborators = fields.List(fields.String())
    can_share = fields.Boolean()
