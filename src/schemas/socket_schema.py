from marshmallow import (
    Schema,
    fields,
    validate,
)


class RoomSchema(Schema):
    room = fields.String(required=True, validate=validate.Length(min=1))


class MessageSchema(RoomSchema):
    message = fields.String(required=True, validate=validate.Length(min=1))
