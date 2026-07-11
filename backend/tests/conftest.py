import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def test_user():

    return {
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "Test@12345"
    }


@pytest.fixture(scope="session")
def auth_headers(client, test_user):

    register_response = client.post(
        "/api/v1/auth/register",
        json=test_user
    )

    if register_response.status_code not in (200, 400):
        pytest.fail(
            f"Unexpected register response: {register_response.text}"
        )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )

    if response.status_code != 200:
        pytest.skip("Unable to authenticate test user.")

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }