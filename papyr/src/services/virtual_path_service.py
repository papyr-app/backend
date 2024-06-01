from bson import ObjectId
from mongoengine import Q
from typing import Dict

from models.virtual_path import VirtualPath
from models.user import User
from models.pdf_document import PDFDocument


def get_virtual_path(virtual_path_id: str) -> VirtualPath:
    return VirtualPath.objects(id=ObjectId(virtual_path_id)).get()


def get_user_virtual_path(user_id: ObjectId, document_id: ObjectId) -> VirtualPath:
    return VirtualPath.objects(Q(user=user_id) & Q(document=document_id)).first()


def create_virtual_path(user: User, document: PDFDocument, file_path: str) -> VirtualPath:
    virtual_path = VirtualPath(
        user=user,
        document=document,
        file_path=file_path
    )
    virtual_path.save()
    return virtual_path


def update_virtual_path(virtual_path: VirtualPath, update_data: Dict):
    virtual_path.file_path = update_data.get('file_path', virtual_path.file_path)
    virtual_path.save()
