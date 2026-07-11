def test_register_validation(client):

    response = client.post(
        "/api/v1/auth/register",
        json={}
    )

    assert response.status_code == 422


def test_invalid_login(client):

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "wrong"
        }
    )

    assert response.status_code == 401