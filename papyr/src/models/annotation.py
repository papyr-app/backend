from mongoengine import Document, ListField, ReferenceField, IntField, StringField, DateTimeField
from datetime import datetime

from models.comment import Comment
from models.pdf_document import PDFDocument
from models.user import User


class Annotation(Document):
    document_id = ReferenceField(PDFDocument, required=True)
    user_id = ReferenceField(User, required=True)
    page_number = IntField(required=True)
    annotation_type = StringField(required=True)
    position = StringField(required=True)
    comments = ListField(ReferenceField(Comment))
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'abstract': True}
