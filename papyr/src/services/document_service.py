from typing import List, Dict
from bson import ObjectId
from datetime import datetime
from mongoengine.errors import NotUniqueError

from errors import AuthorizationError
from models.pdf_document import PDFDocument
from models.user import User


def get_document(document_id: ObjectId) -> PDFDocument:
    return PDFDocument.objects(id=document_id).get()


def get_document_check_access(document_id: int, user_id: ObjectId):
    document = PDFDocument.objects(id=ObjectId(document_id)).get()
    if not document.has_access(user_id):
        raise AuthorizationError('You are not authorized to access this resource')
    return document


def get_documents_by_owner(user_id: ObjectId) -> List[PDFDocument]:
    return list(PDFDocument.objects(owner=user_id).all())


def get_documents_by_collaborator(user_id: ObjectId) -> List[PDFDocument]:
    return list(PDFDocument.objects(collaborators=user_id).all())


def create_document(owner_id: int, file_path: str, title: str, description: str) -> PDFDocument:
    if PDFDocument.objects(file_path=file_path).first():
        raise NotUniqueError('Document with this title already exists')

    new_document = PDFDocument(
        owner=owner_id,
        file_path=file_path,
        title=title,
        description=description
    )
    new_document.save()
    return new_document


def update_document(document: PDFDocument, document_data: Dict) -> PDFDocument:
    document.title = document_data.get('title', document.title)
    document.description = document_data.get('description', document.description)
    document.file_path = document_data.get('file_path', document.file_path)
    document.can_share = document_data.get('can_share', document.can_share)
    document.updated_at = datetime.utcnow()
    document.save()
    return document


def delete_document(document: PDFDocument):
    document.delete()


def add_collaborator(user: User, document: PDFDocument) -> PDFDocument:
    if user not in document.collaborators:
        document.collaborators.append(user)
        document.save()
    return document


def remove_collaborator(user: User, document: PDFDocument) -> PDFDocument:
    if user in document.collaborators:
        document.collaborators.remove(user)
        document.save()
    return document
