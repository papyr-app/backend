from bson import ObjectId

from models.comment import Comment


def get_comment(comment_id: int) -> Comment:
    return Comment.objects(id=ObjectId(comment_id)).get()


def create_comment() -> Comment:
    pass


def update_comment() -> Comment:
    pass


def delete_comment(comment_id: int):
    comment = get_comment(comment_id)
    comment.delete()
