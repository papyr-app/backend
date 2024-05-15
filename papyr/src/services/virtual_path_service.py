from bson import ObjectId
from mongoengine import Q
from typing import Dict

from models.virtual_path import VirtualPath


def get_virtual_path(virtual_path_id: str) -> VirtualPath:
    return VirtualPath.objects(id=ObjectId(virtual_path_id)).get()


def get_user_virtual_path(user_id: ObjectId, document_id: ObjectId) -> VirtualPath:
    return VirtualPath.objects(Q(user=user_id) & Q(document=document_id)).first()


def update_virtual_path(virtual_path: VirtualPath, update_data: Dict):
    # TODO - make sure path is ok
    virtual_path.file_path = update_data.get('update_data', virtual_path.file_path)
    virtual_path.save()
