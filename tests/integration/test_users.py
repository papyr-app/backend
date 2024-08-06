from flask.testing import FlaskClient


def test_get_user(client: FlaskClient, helpers):
    user, user_auth = helpers.create_user_and_login(client)

    response = client.get("/users", headers=user_auth)
    assert response.status_code == 200
    assert response.json["data"]["username"] == user.username


def test_update_user(client: FlaskClient, helpers):
    user, user_auth = helpers.create_user_and_login(client)

    response = client.patch("/users", json={"first_name": "Updated"}, headers=user_auth)
    assert response.status_code == 200
    assert response.json["data"]["first_name"] == "Updated"


def test_get_user_documents(client: FlaskClient, helpers):
    user, user_auth = helpers.create_user_and_login(client)
    helpers.create_pdf_document(user)

    response = client.get("/users/documents", headers=user_auth)
    assert response.status_code == 200
    assert len(response.json["data"]) == 1
