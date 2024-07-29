from marshmallow import (
    Schema,
    fields,
    validate,
)


class SocketSchema(Schema):
    token = fields.String(required=True, validate=validate.Length(min=1))


class RoomSchema(SocketSchema):
    room = fields.String(required=True, validate=validate.Length(min=1))


class MessageSchema(SocketSchema):
    message = fields.String(required=True, validate=validate.Length(min=1))
