from typing import List, Dict
from bson import ObjectId
from datetime import datetime
from mongoengine import Q

from errors import AuthorizationError
from models.pdf_document import PDFDocument
from models.user import User


def get_document(document_id: ObjectId) -> PDFDocument:
    return PDFDocument.objects(id=document_id).get()


def get_document_by_share_token(share_token: str) -> PDFDocument:
    return PDFDocument.objects(share_token=share_token).get()


def get_document_check_access(document_id: int, user_id: ObjectId) -> PDFDocument:
    """
    Retrieves a PDF document and checks if the user has access to it.

    :param document_id: The ID of the document to retrieve.
    :type document_id: int
    :param user_id: The ID of the user requesting access to the document.
    :type user_id: ObjectId
    :raises AuthorizationError: If the user does not have access to the document.
    :return: The PDF document if access is granted.
    :rtype: PDFDocument
    """
    document = PDFDocument.objects(id=ObjectId(document_id)).get()
    if not document.has_access(user_id):
        raise AuthorizationError()
    return document


def get_user_documents(user_id: ObjectId) -> List[PDFDocument]:
    return list(PDFDocument.objects(Q(owner=user_id) | Q(collaborators=user_id)).all())


def create_document(owner_id: int, title: str, description: str) -> PDFDocument:
    new_document = PDFDocument(owner=owner_id, title=title, description=description)
    new_document.save()
    return new_document


def update_document(document: PDFDocument, document_data: Dict) -> PDFDocument:
    document.title = document_data.get("title", document.title)
    document.description = document_data.get("description", document.description)
    document.can_share = document_data.get("can_share", document.can_share)
    document.updated_at = datetime.utcnow()
    document.save()
    return document


def delete_document(document: PDFDocument):
    document.delete()


def add_collaborator(user: User, document: PDFDocument) -> PDFDocument:
    """
    Adds a user as a collaborator to a PDF document if they are not already a collaborator and are not the owner.

    :param user: The user to be added as a collaborator.
    :type user: User
    :param document: The PDF document to which the user will be added as a collaborator.
    :type document: PDFDocument
    :return: The updated PDF document with the new collaborator.
    :rtype: PDFDocument
    """
    if user not in document.collaborators and user != document.owner:
        document.collaborators.append(user)
        document.updated_at = datetime.utcnow()
        document.save()
    return document


def remove_collaborator(user: User, document: PDFDocument) -> PDFDocument:
    """
    Removes a user from the collaborators of a PDF document if they are a collaborator and are not the owner.

    :param user: The user to be removed from the collaborators.
    :type user: User
    :param document: The PDF document from which the user will be removed as a collaborator.
    :type document: PDFDocument
    :return: The updated PDF document with the collaborator removed.
    :rtype: PDFDocument
    """
    if user in document.collaborators and user != document.owner:
        document.collaborators.remove(user)
        document.updated_at = datetime.utcnow()
        document.save()
    return document
