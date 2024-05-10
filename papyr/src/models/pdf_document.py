from mongoengine import Document, ListField, StringField, ReferenceField, DateTimeField
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
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'pdf_documents',
        'indexes': [
            'title',
        ],
        'ordering': ['-created_at']
    }
