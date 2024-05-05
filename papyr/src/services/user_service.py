from models.user import User


def get_user(username):
    user = User.objects(username=username).first()
    return user


def create_user(user_data):
    if User.objects(username=user_data['username']).first():
        raise ValueError('Username already exists')

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
