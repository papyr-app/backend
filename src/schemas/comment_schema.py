from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, ValidationError

from models import Comment


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True
        include_fk = True


class CreateCommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True
        include_fk = True

    document_id = fields.Str(required=True)
    user_id = fields.Str(required=True)
    text = fields.Str(required=True)


class UpdateCommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True
        include_fk = True

    id = fields.Str(required=True)
    text = fields.Str(required=False)

    @validates("id")
    def validate_id(self, value):
        if not Comment.query.get(value):
            raise ValidationError("Comment not found.")
