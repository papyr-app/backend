from mongoengine import Document, StringField, DateTimeField
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class User(Document):
    username = StringField(primary_key=True)
    email = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    role = StringField(required=True)
    password_hash = StringField()
    created_at = DateTimeField(required=True)
    last_login = DateTimeField()

    meta = {"collection": "users"}

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
