from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime, timedelta

from models.user import User
from models.pdf_document import PDFDocument


class Invitation(Document):
    invite_id = StringField(required=True)
    document = ReferenceField(PDFDocument, required=True)
    invited_by = ReferenceField(User, required=True)
    expires_at = DateTimeField(default=lambda: datetime.now() + timedelta(days=7))

    meta = {
        'collection': 'invitations',
        'ordering': ['-expires_at']
    }
