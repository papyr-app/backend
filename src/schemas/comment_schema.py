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
    document_id = fields.Str(required=True)
    user_id = fields.Str(required=True)
    text = fields.Str(required=True)


class UpdateCommentSchema(Schema):
    id = fields.Str(required=True)
    text = fields.Str(required=False)

    @validates("id")
    def validate_id(self, value):
        if not Comment.query.get(value):
            raise ValidationError("Comment not found.")
