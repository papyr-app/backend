from flask.testing import FlaskClient

from src.models import User


def test_register_user(client: FlaskClient):
    response = client.post(
        "/auth/register",
        json={
            "username": "test",
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "Mc. Test",
            "password": "123456",
        },
    )
    assert response.status_code == 201

    user = User.query.filter_by(username="test").first()
    assert user is not None


def test_register_user_missing_fields(client: FlaskClient):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "Mc. Test",
            "password": "123456",
        },
    )
    assert response.status_code == 400

    user = User.query.filter_by(last_name="Mc. Test").first()
    assert user is None


def test_register_user_short_password(client: FlaskClient):
    response = client.post(
        "/auth/register",
        json={
            "username": "test",
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "Mc. Test",
            "password": "123",
        },
    )
    assert response.status_code == 400

    user = User.query.filter_by(username="test").first()
    assert user is None


def test_register_and_login_successfully(client: FlaskClient):
    response = client.post(
        "/auth/register",
        json={
            "username": "test",
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "Mc. Test",
            "password": "123456",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/auth/login", json={"username": "test", "password": "123456"}
    )
    assert response.status_code == 200

    access_token = response.json.get("data")
    assert access_token is not None


def test_register_and_login_wrong_password(client: FlaskClient):
    response = client.post(
        "/auth/register",
        json={
            "username": "test",
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "Mc. Test",
            "password": "123456",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/auth/login", json={"username": "test", "password": "1234567"}
    )
    assert response.status_code == 401
