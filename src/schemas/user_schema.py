from marshmallow import Schema, fields, validate, validates, ValidationError
from models.user import User


class CreateUserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=2, max=20))
    email = fields.Email(required=True)
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=20))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=20))
    password = fields.String(required=True, load_only=True)

    @validates("username")
    def validate_username(self, value):
        if User.objects(username=value).first():
            raise ValidationError("Username already exists.")

    @validates("email")
    def validate_email(self, value):
        if User.objects(email=value).first():
            raise ValidationError("Email already exists.")

    @validates("password")
    def validate_password(self, value):
        # TODO - add more logic to make sure password is complex
        if len(value) < 6:
            raise ValidationError("Password must be at least 6 characters long.")


class UpdateUserSchema(Schema):
    username = fields.String(required=False, validate=validate.Length(min=2, max=20))
    email = fields.Email(required=False)
    first_name = fields.String(required=False, validate=validate.Length(min=2, max=20))
    last_name = fields.String(required=False, validate=validate.Length(min=2, max=20))

    @validates("username")
    def validate_username(self, value):
        if User.objects(username=value).first():
            raise ValidationError("Username already exists.")

    @validates("email")
    def validate_email(self, value):
        if User.objects(email=value).first():
            raise ValidationError("Email already exists.")
