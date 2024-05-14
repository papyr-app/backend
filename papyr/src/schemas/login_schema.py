from marshmallow import Schema, fields, validates, validate, ValidationError


class LoginSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))

    @validates('password')
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError('Password must be at least 6 characters long')
