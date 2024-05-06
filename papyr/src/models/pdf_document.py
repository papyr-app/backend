from mongoengine import Document, ListField, StringField, ReferenceField, DateTimeField
from datetime import datetime
from models.user import User


class PDFDocument(Document):
    owner = ReferenceField(User, required=True)
    file_path = StringField(required=True)
    title = StringField(required=True)
    description = StringField()
    collaborators = ListField(ReferenceField(User))
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'pdf_documents',
        'indexes': [
            'title',
            'owner_id'
        ],
        'ordering': ['-created_at']
    }
