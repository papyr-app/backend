from typing import Dict
from datetime import datetime
from bson import ObjectId
from mongoengine.errors import NotUniqueError

from models.user import User


def get_user_by_id(user_id: ObjectId) -> User:
    return User.objects(id=user_id).get()


def get_user_by_username(username: str) -> User:
    return User.objects(username=username).get()


def get_user_by_email(email: str):
    return User.objects(email=email).get()


def create_user(username: str, email: str, first_name: str, last_name: str, role: str, password: str) -> User:
    if User.objects(username=username).first():
        raise NotUniqueError('Username already exists')

    if User.objects(email=email).first():
        raise NotUniqueError('Email already exists')

    new_user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=role,
    )
    new_user.set_password(password)
    new_user.save()
    return new_user


def update_user(user: User, user_data: Dict) -> User:
    user.first_name = user_data.get('first_name', user.first_name)
    user.last_name = user_data.get('last_name', user.last_name)
    user.last_updated = datetime.utcnow()
    user.save()
    return user
