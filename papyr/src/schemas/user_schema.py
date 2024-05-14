from marshmallow import Schema, fields, validate, validates, ValidationError


class CreateUserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    first_name = fields.String(required=True, validate=validate.Length(min=1))
    last_name = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))
    role = fields.String(validate=validate.Length(min=1))
    created_at = fields.DateTime(dump_only=True)
    last_updated = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True)

    @validates('password')
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError('Password must be at least 6 characters long')


class UpdateUserSchema(Schema):
    username = fields.String(validate=validate.Length(min=1))
    email = fields.Email()
    first_name = fields.String(validate=validate.Length(min=1))
    last_name = fields.String(validate=validate.Length(min=1))
    role = fields.String(validate=validate.Length(min=1))
    password = fields.String(load_only=True, validate=validate.Length(min=6))
    last_login = fields.DateTime()

    @validates('password')
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError('Password must be at least 6 characters long')
