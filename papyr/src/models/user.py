from mongoengine import Document, StringField, DateTimeField
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()


class User(Document):
    username = StringField(required=True)
    email = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    role = StringField(required=True)
    password_hash = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'users',
            'indexes': [
                'username',
                'email'
            ],
            'ordering': ['-created_at']
            }

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
