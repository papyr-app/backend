import logging
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from models import VirtualPath


class VirtualPathService:
    @staticmethod
    def get_virtual_path_by_id(user_id: int) -> User:
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValidationError("User not found.")
            return user
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise
