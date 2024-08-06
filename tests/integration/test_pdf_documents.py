from io import BytesIO
from flask.testing import FlaskClient
from moto import mock_aws

from src.app import db
from src.models import PDFDocument, VirtualPath


@mock_aws
def test_create_document(client: FlaskClient, helpers):
    user, user_auth = helpers.create_user_and_login(client)
    helpers.create_s3_bucket(client)

    data = {
        "file": (BytesIO(b"File content."), "file.pdf"),
        "title": "Test Title",
        "description": "This is a test file.",
        "can_share": True,
        "file_path": "/2024",
    }

    response = client.post(
        "/documents", data=data, content_type="multipart/form-data", headers=user_auth
    )
    assert response.status_code == 201
    assert len(PDFDocument.query.all()) == 1
    assert PDFDocument.query.filter_by(title="Test Title").first() is not None


@mock_aws
def test_get_document(client: FlaskClient, helpers):
    user, user_auth = helpers.create_user_and_login(client)
    document = helpers.create_pdf_document(user)

    response = client.get(f"/documents/{document.id}", headers=user_auth)
    assert response.status_code == 200
    assert response.json["data"]["owner_id"] == user.id
    assert response.json["data"]["title"] == document.title


@mock_aws
def test_create_and_download_document(client: FlaskClient, helpers):
    user, user_auth = helpers.create_user_and_login(client)
    helpers.create_s3_bucket(client)

    data = {
        "file": (BytesIO(b"File content."), "file.pdf"),
        "title": "Test Title",
        "description": "This is a test file.",
        "can_share": True,
        "file_path": "/2024",
    }

    response = client.post(
        "/documents", data=data, content_type="multipart/form-data", headers=user_auth
    )
    assert response.status_code == 201

    response = client.get(
        f"/documents/{response.json['data']['id']}/download", headers=user_auth
    )
    assert response.status_code == 200
    assert response.data == b"File content."


@mock_aws
def test_update_document(client: FlaskClient, helpers):
    user, user_auth = helpers.create_user_and_login(client)
    document = helpers.create_pdf_document(user)

    response = client.patch(
        f"/documents/{document.id}",
        json={"title": "Updated Title", "file_path": "/updated_path"},
        headers=user_auth,
    )
    assert response.status_code == 200
    assert PDFDocument.query.get(document.id).title == "Updated Title"
    assert (
        VirtualPath.query.filter_by(document_id=document.id, user_id=user.id)
        .first()
        .file_path
        == "/updated_path"
    )


@mock_aws
def test_delete_document(client: FlaskClient, helpers):
    user, user_auth = helpers.create_user_and_login(client)
    helpers.create_s3_bucket(client)

    data = {
        "file": (BytesIO(b"File content."), "file.pdf"),
        "title": "Test Title",
        "description": "This is a test file.",
        "can_share": True,
        "file_path": "/2024",
    }

    response = client.post(
        "/documents", data=data, content_type="multipart/form-data", headers=user_auth
    )
    assert response.status_code == 201
    assert len(PDFDocument.query.all()) == 1

    response = client.delete(
        f"/documents/{response.json['data']['id']}",
        headers=user_auth,
    )
    assert response.status_code == 200
    assert len(PDFDocument.query.all()) == 0


def test_add_collaborator(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    user2, user2_auth = helpers.create_user_and_login(client)
    document = helpers.create_pdf_document(user1)

    assert len(document.collaborators) == 0

    response = client.post(
        f"/documents/{document.id}/add_collaborator",
        json={"email": user2.email},
        headers=user1_auth,
    )
    assert response.status_code == 200
    assert len(document.collaborators) == 1


def test_remove_collaborator(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    user2, user2_auth = helpers.create_user_and_login(client)
    document = helpers.create_pdf_document(user1)

    document.collaborators.append(user2)
    db.session.commit()

    assert len(document.collaborators) == 1

    response = client.post(
        f"/documents/{document.id}/remove_collaborator",
        json={"email": user2.email},
        headers=user1_auth,
    )
    assert response.status_code == 200
    assert len(document.collaborators) == 0


def test_use_share_token_shareable(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    user2, user2_auth = helpers.create_user_and_login(client)
    document = helpers.create_pdf_document(user1)

    document.can_share = True
    db.session.commit()

    response = client.post(
        f"/documents/share/{document.share_token}",
        headers=user2_auth,
    )
    assert response.status_code == 200
    assert len(document.collaborators) == 1


def test_use_share_token_not_shareable(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    user2, user2_auth = helpers.create_user_and_login(client)
    document = helpers.create_pdf_document(user1)

    document.can_share = False
    db.session.commit()

    response = client.post(
        f"/documents/share/{document.share_token}",
        headers=user2_auth,
    )
    assert response.status_code == 400
    assert len(document.collaborators) == 0
