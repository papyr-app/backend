from marshmallow import (
    Schema,
    fields,
    validate,
)


class MessageSchema(Schema):
    message = fields.String(required=True, validate=validate.Length(min=1))
