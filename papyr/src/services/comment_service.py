from typing import Dict
from datetime import datetime
from bson import ObjectId

from models.pdf_document import PDFDocument
from models.user import User
from models.comment import Comment


def get_comment(comment_id: int) -> Comment:
    return Comment.objects(id=ObjectId(comment_id)).get()


def create_comment(document: PDFDocument, user: User, text: str) -> Comment:
    comment = Comment(
            document=document,
            user=user,
            text=text
    )
    comment.save()
    return comment


def update_comment(comment: Comment, comment_data: Dict) -> Comment:
    comment.text = comment_data.get('text', comment.text)
    comment.updated_at = datetime.utcnow()
    comment.save()
    return comment


def delete_comment(comment_id: int):
    comment = get_comment(comment_id)
    comment.delete()
