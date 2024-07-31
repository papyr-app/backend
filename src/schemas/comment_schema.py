from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields, validates, ValidationError

from src.app import db
from src.models import Comment


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True
        include_fk = True
        sqla_session = db.session


class CreateCommentSchema(Schema):
    document_id = fields.String(required=True)
    user_id = fields.String(required=True)
    text = fields.String(required=True)


class UpdateCommentSchema(Schema):
    id = fields.String(required=True)
    text = fields.String(required=False)

    @validates("id")
    def validate_id(self, value):
        if not Comment.query.get(value):
            raise ValidationError("Comment not found.")
