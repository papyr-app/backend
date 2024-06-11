import logging
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from marshmallow import ValidationError

from app import db
from schemas.comment_schema import CreateCommentSchema, UpdateCommentSchema
from models.comment import Comment


class CommentService:
    @staticmethod
    def create_comment(data):
        schema = CreateCommentSchema()
        try:
            validated_data = schema.load(data)
            comment = Comment(**validated_data)
            db.session.add(comment)
            db.session.commit()
            return comment
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def update_comment(comment_id, data):
        schema = UpdateCommentSchema()
        try:
            comment = Comment.query.get(comment_id)
            validated_data = schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(comment, key, value)
            db.session.commit()
            return comment
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def delete_comment(comment_id):
        try:
            comment = Comment.query.get(comment_id)
            if not comment:
                raise ValidationError("Comment not found.")
            db.session.delete(comment)
            db.session.commit()
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"SQLAlchemy error: {str(e)}")
            raise
