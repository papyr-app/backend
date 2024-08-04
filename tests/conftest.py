import pytest

from src.app import init_app


@pytest.fixture(scope="function")
def client():
    app = init_app("src.config.TestingConfig")
    client = app.test_client()

    with app.app_context():
        yield client
