from marshmallow import Schema, fields, validate, validates, ValidationError

from models.user import User


class LoginSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=2, max=20))
    password = fields.String(
        required=True, load_only=True, validate=validate.Length(min=6)
    )

    @validates("username")
    def validate_username(self, value):
        if User.query.filter_by(username=value).first() is None:
            raise ValidationError("Invalid username or password")
