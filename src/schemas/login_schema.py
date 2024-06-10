from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=2, max=20))
    password = fields.String(
        required=True, load_only=True, validate=validate.Length(min=6)
    )
