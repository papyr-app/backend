import logging
from typing import Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from marshmallow import ValidationError

from app import db
from models import User
from schemas.user_schema import CreateUserSchema, UpdateUserSchema
from schemas.login_schema import LoginSchema
from auth.jwt_handler import generate_jwt


class UserService:
    @staticmethod
    def create_user(data: Dict[str, Any]) -> User:
        schema = CreateUserSchema()
        try:
            validated_data = schema.load(data)
            password = validated_data.pop("password")
            user = User(**validated_data)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return user
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def update_user(user_id: int, data: Dict[str, Any]) -> User:
        schema = UpdateUserSchema()
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValidationError("User not found.")
            validated_data = schema.load(data, partial=True)
            if "password" in validated_data:
                user.set_password(validated_data.pop("password"))
            for key, value in validated_data.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def delete_user(user_id: int) -> None:
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValidationError("User not found.")
            db.session.delete(user)
            db.session.commit()
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValidationError("User not found.")
            return user
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def get_user_by_username(username: str) -> User:
        try:
            user = User.query.filter_by(username=username).first()
            if not user:
                raise ValidationError("User not found.")
            return user
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def get_user_by_email(email: str) -> User:
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                raise ValidationError("User not found.")
            return user
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy error: {str(e)}")
            raise

    @staticmethod
    def login(data: Dict[str, Any]) -> str:
        schema = LoginSchema()
        try:
            validated_data = schema.load(data)
            user = UserService.get_user_by_username(validated_data["username"])
            if user and user.check_password(validated_data["password"]):
                user.record_login()
                return generate_jwt(str(user.id))
            else:
                raise ValidationError("Invalid username or password")
        except ValidationError as e:
            logging.error(f"Validation error: {e.messages}")
            raise
        except Exception as e:
            logging.error(f"Exception: {str(e)}")
            raise
