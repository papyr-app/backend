from mongoengine import Document, ReferenceField, StringField, DateTimeField
from datetime import datetime

from models.pdf_document import PDFDocument
from models.user import User


class Comment(Document):
    document = ReferenceField(PDFDocument, required=True)
    user = ReferenceField(User, required=True)
    text = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "comments"}
