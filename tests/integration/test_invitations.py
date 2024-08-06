import uuid
from flask.testing import FlaskClient

from src.app import db
from src.models import Invitation


def test_create_invite(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    user2, user2_auth = helpers.create_user_and_login(client)
    pdf_document = helpers.create_pdf_document(user1)

    response = client.post(
        "/invitation/invite",
        json={"document_id": pdf_document.id, "invitee": user2.email},
        headers=user1_auth,
    )
    assert response.status_code == 201
    assert len(Invitation.query.all()) == 1
    assert (
        db.session.query(Invitation).filter_by(invited_by_id=user1.id).first()
        is not None
    )
    assert (
        db.session.query(Invitation).filter_by(invitee_id=user2.id).first() is not None
    )


def test_get_invite(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    user2, user2_auth = helpers.create_user_and_login(client)
    pdf_document = helpers.create_pdf_document(user1)

    invitation = Invitation(
        document_id=pdf_document.id, invited_by_id=user1.id, invitee_id=user2.id
    )
    db.session.add(invitation)
    db.session.commit()

    response = client.get(
        f"/invitation/{invitation.id}",
        headers=user1_auth,
    )
    assert response.status_code == 200
    assert response.json["data"]["invited_by_id"] == user1.id
    assert response.json["data"]["invitee_id"] == user2.id
    assert response.json["data"]["document_id"] == pdf_document.id


def test_get_sent_invitations(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    user2, user2_auth = helpers.create_user_and_login(client)
    pdf_document = helpers.create_pdf_document(user1)

    invitation = Invitation(
        document_id=pdf_document.id, invited_by_id=user1.id, invitee_id=user2.id
    )

    db.session.add(invitation)
    db.session.commit()

    response = client.get(
        "/invitation/sent",
        headers=user1_auth,
    )
    assert response.status_code == 200
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["invited_by_id"] == user1.id
    assert response.json["data"][0]["invitee_id"] == user2.id


def test_get_received_invitations(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    user2, user2_auth = helpers.create_user_and_login(client)
    pdf_document = helpers.create_pdf_document(user1)

    invitation = Invitation(
        document_id=pdf_document.id, invited_by_id=user1.id, invitee_id=user2.id
    )

    db.session.add(invitation)
    db.session.commit()

    response = client.get(
        "/invitation/received",
        headers=user2_auth,
    )
    assert response.status_code == 200

    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["invited_by_id"] == user1.id
    assert response.json["data"][0]["invitee_id"] == user2.id


def test_accept_invitation(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    user2, user2_auth = helpers.create_user_and_login(client)
    pdf_document = helpers.create_pdf_document(user1)

    invitation = Invitation(
        document_id=pdf_document.id, invited_by_id=user1.id, invitee_id=user2.id
    )

    db.session.add(invitation)
    db.session.commit()

    assert len(pdf_document.collaborators) == 0

    response = client.post(
        f"/invitation/accept/{invitation.id}",
        headers=user2_auth,
    )
    assert response.status_code == 200
    assert len(pdf_document.collaborators) == 1
    assert response.json["data"]["invited_by_id"] == user1.id
    assert response.json["data"]["invitee_id"] == user2.id


def test_invite_invalid_document(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    user2, user2_auth = helpers.create_user_and_login(client)

    response = client.post(
        "/invitation/invite",
        json={"document_id": str(uuid.uuid4()), "invitee": user2.email},
        headers=user1_auth,
    )
    assert response.status_code == 400
    assert len(Invitation.query.all()) == 0


def test_invite_invalid_user(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    pdf_document = helpers.create_pdf_document(user1)

    response = client.post(
        "/invitation/invite",
        json={"document_id": pdf_document.id, "invitee": "idontexist@gmail.com"},
        headers=user1_auth,
    )
    assert response.status_code == 400
    assert len(Invitation.query.all()) == 0


def test_invite_twice(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    user2, user2_auth = helpers.create_user_and_login(client)
    pdf_document = helpers.create_pdf_document(user1)

    response = client.post(
        "/invitation/invite",
        json={"document_id": pdf_document.id, "invitee": user2.email},
        headers=user1_auth,
    )
    assert response.status_code == 201
    assert len(Invitation.query.all()) == 1

    response = client.post(
        "/invitation/invite",
        json={"document_id": pdf_document.id, "invitee": user2.email},
        headers=user1_auth,
    )
    assert response.status_code == 400
    assert len(Invitation.query.all()) == 1


def test_invite_self(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    pdf_document = helpers.create_pdf_document(user1)

    response = client.post(
        "/invitation/invite",
        json={"document_id": pdf_document.id, "invitee": user1.email},
        headers=user1_auth,
    )
    assert response.status_code == 400
    assert len(Invitation.query.all()) == 0


def test_invite_existing_collaborator(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    user2, user2_auth = helpers.create_user_and_login(client)
    pdf_document = helpers.create_pdf_document(user1)

    response = client.post(
        "/invitation/invite",
        json={"document_id": pdf_document.id, "invitee": user2.email},
        headers=user1_auth,
    )
    assert response.status_code == 201

    response = client.post(
        f"/invitation/accept/{response.json['data']['id']}",
        headers=user2_auth,
    )
    assert response.status_code == 200
    assert len(pdf_document.collaborators) == 1

    response = client.post(
        "/invitation/invite",
        json={"document_id": pdf_document.id, "invitee": user2.email},
        headers=user1_auth,
    )
    assert response.status_code == 400
    assert len(pdf_document.collaborators) == 1


def test_invite_without_access(client: FlaskClient, helpers):
    user1, user1_auth = helpers.create_user_and_login(client)
    user2, user2_auth = helpers.create_user_and_login(client)
    pdf_document = helpers.create_pdf_document(user1)

    response = client.post(
        "/invitation/invite",
        json={"document_id": pdf_document.id, "invitee": user1.email},
        headers=user2_auth,
    )
    assert response.status_code == 403
    assert len(Invitation.query.all()) == 0
