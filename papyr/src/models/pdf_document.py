import uuid
from mongoengine import Document, ListField, StringField, ReferenceField, DateTimeField, BooleanField
from datetime import datetime

from models.user import User
from const import DocumentStatus


class PDFDocument(Document):
    owner = ReferenceField(User, required=True)
    file_path = StringField(required=True)
    title = StringField(required=True)
    description = StringField()
    status = StringField(default=DocumentStatus.ACTIVE)
    collaborators = ListField(ReferenceField(User))
    can_share = BooleanField(default=False)
    share_token = StringField(default=lambda: str(uuid.uuid4()), unique=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'pdf_documents',
        'indexes': [
            'title',
        ],
        'ordering': ['-created_at']
    }
