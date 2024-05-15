from bson import ObjectId
from mongoengine import Q

from models.virtual_path import VirtualPath


def get_user_virtual_path(user_id: ObjectId, document_id: ObjectId) -> VirtualPath:
    return VirtualPath.objects(Q(user=user_id) & Q(document=document_id)).first()
