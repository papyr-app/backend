from mongoengine import Document, StringField, DateTimeField
from flask_bcrypt import Bcrypt
from datetime import datetime

from const import RoleType

bcrypt = Bcrypt()


class User(Document):
    username = StringField(required=True)
    email = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    password_hash = StringField()
    role = StringField(default=RoleType.USER)
    created_at = DateTimeField(default=datetime.utcnow)
    last_updated = DateTimeField(default=datetime.utcnow)
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

    def record_login(self):
        self.last_login = datetime.utcnow()
        self.save()

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return data
