from mongoengine.errors import NotUniqueError
from models.user import User


def get_user_by_username(username: str):
    return User.objects(username=username).get()


def get_user_by_email(email: str):
    return User.objects(email=email).get()


def create_user(user_data):
    if User.objects(username=user_data['username']).first():
        raise NotUniqueError('Username already exists')

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
