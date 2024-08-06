import os
import sys
import random
import string
import pytest
import boto3
from moto import mock_aws
from typing import Dict, Tuple, Any
from flask.testing import FlaskClient

from src.app import init_app, db
from src.models import User, PDFDocument

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)


@pytest.fixture(scope="function")
def client():
    app = init_app("src.config.TestingConfig")
    client = app.test_client()

    with app.app_context():
        yield client
        db.session.remove()
        db.drop_all()


class Helpers:
    def get_random_string(length: int) -> str:
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @staticmethod
    def create_user_and_login(client: FlaskClient) -> Tuple[User, Dict[str, Any]]:
        username = Helpers.get_random_string(4)
        password = Helpers.get_random_string(6)

        user = User(
            username=username,
            email=f"{username}@gmail.com",
            first_name=username,
            last_name=username,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        response = client.post(
            "/auth/login", json={"username": username, "password": password}
        )
        assert response.status_code == 200
        access_token = response.json["data"]

        return user, {"Authorization": f"{access_token}"}

    @staticmethod
    def create_pdf_document(owner: User) -> PDFDocument:
        document = PDFDocument(
            owner_id=owner.id,
            title="Test Document",
            description="A test document description",
            can_share=True,
        )

        db.session.add(document)
        db.session.commit()

        return document

    @staticmethod
    @mock_aws
    def create_s3_bucket(client: FlaskClient):
        bucket_name = client.application.config.get("S3_BUCKET_NAME")
        conn = boto3.resource("s3", region_name="eu-north-1")

        conn.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-north-1"},
        )


@pytest.fixture
def helpers():
    return Helpers
