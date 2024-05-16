from marshmallow import Schema, fields, validate


class CreatePDFDocumentSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(missing=None)


class UpdatePDFDocumentSchema(Schema):
    title = fields.String(validate=validate.Length(min=1))
    description = fields.String()
    status = fields.String()
    collaborators = fields.List(fields.String())
    can_share = fields.Boolean()
