from bson import ObjectId
from mongoengine.errors import NotUniqueError
from models.user import User


def get_user_by_id(user_id: int):
    return User.objects(id=ObjectId(user_id)).get()


def get_user_by_username(username: str):
    return User.objects(username=username).get()


def get_user_by_email(email: str):
    return User.objects(email=email).get()


def create_user(user_data):
    # TODO - pass arguments instead of user_data dict
    if User.objects(username=user_data['username']).first():
        raise NotUniqueError('Username already exists')

    if User.objects(email=user_data['email']).first():
        raise NotUniqueError('Email already exists')

    new_user = User(
        username=user_data['username'],
        email=user_data['email'],
        first_name=user_data.get('first_name', ''),
        last_name=user_data.get('last_name', ''),
        role=user_data.get('role', 'User'),
    )
    new_user.set_password(user_data['password'])
    new_user.save()
    return new_user
