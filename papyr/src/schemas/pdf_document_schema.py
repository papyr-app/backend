from marshmallow import Schema, fields, validate, validates, ValidationError

from const import DocumentStatus


class CreatePDFDocumentSchema(Schema):
    file_path = fields.String(required=True, validate=validate.Length(min=1))
    title = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(missing=None)


class UpdatePDFDocumentSchema(Schema):
    file_path = fields.String(validate=validate.Length(min=1))
    title = fields.String(validate=validate.Length(min=1))
    description = fields.String()
    status = fields.String()
    collaborators = fields.List(fields.String())
    can_share = fields.Boolean()
