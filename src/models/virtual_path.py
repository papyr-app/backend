from mongoengine import Document, ReferenceField, StringField

from models.user import User
from models.pdf_document import PDFDocument


class VirtualPath(Document):
    user = ReferenceField(User, required=True)
    document = ReferenceField(PDFDocument, required=True)
    file_path = StringField(required=True)

    meta = {'collection': 'virtual_paths'}
