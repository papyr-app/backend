import logging
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from marshmallow import ValidationError

from app import db
from schemas.virtual_path_schema import CreateVirtualPathSchema, UpdateVirtualPathSchema
from models import VirtualPath


class VirtualPathService:
    @staticmethod
    def create_virtual_path(data):
        schema = CreateVirtualPathSchema()
        try:
            validated_data = schema.load(data)
            virtual_path = VirtualPath(**validated_data)
            db.session.add(virtual_path)
            db.session.commit()
            return virtual_path
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def update_virtual_path(virtual_path_id, data):
        schema = UpdateVirtualPathSchema()
        try:
            virtual_path = VirtualPath.query.get(virtual_path_id)
            if not virtual_path:
                raise ValidationError("VirtualPath not found.")
            validated_data = schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(virtual_path, key, value)
            db.session.commit()
            return virtual_path
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def delete_virtual_path(virtual_path_id):
        try:
            virtual_path = VirtualPath.query.get(virtual_path_id)
            if not virtual_path:
                raise ValidationError("VirtualPath not found.")
            db.session.delete(virtual_path)
            db.session.commit()
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"SQLAlchemy error: {str(e)}")
            raise
