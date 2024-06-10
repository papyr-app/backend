from typing import Dict, Any
from dataclasses import dataclass, asdict
from bson import ObjectId

from services import virtual_path_service


@dataclass
class PDFDocumentDTO:
    _id: str
    title: str
    description: str
    status: str
    owner: Dict[str, Any]
    can_share: bool
    share_token: str
    file_path: str
    is_owner: bool
    created_at: str
    updated_at: str

    def to_dict(self):
        return asdict(self)


def create_pdf_document_dto(
    document: Dict[str, Any], user_id: ObjectId
) -> PDFDocumentDTO:
    is_owner = document["owner"]["_id"] == user_id

    virtual_path = virtual_path_service.get_user_virtual_path(user_id, document["_id"])
    if virtual_path:
        file_path = f'{virtual_path.file_path}/{document["title"]}'
    else:
        file_path = document["title"]

    return PDFDocumentDTO(
        _id=document["_id"],
        title=document["title"],
        description=document["description"],
        status=document["status"],
        owner=document["owner"],
        can_share=document["can_share"],
        share_token=document["share_token"],
        file_path=file_path,
        is_owner=is_owner,
        created_at=document["created_at"],
        updated_at=document["updated_at"],
    )
