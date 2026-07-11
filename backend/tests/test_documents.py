from io import BytesIO


def test_upload_requires_auth(client):

    response = client.post(
        "/api/v1/documents/upload"
    )

    assert response.status_code in (401, 403)


def test_upload_with_auth(client, auth_headers):

    fake_file = BytesIO(b"Hello World")

    response = client.post(
        "/api/v1/documents/upload",
        headers=auth_headers,
        files={
            "file": (
                "sample.txt",
                fake_file,
                "text/plain"
            )
        }
    )

    assert response.status_code in (200, 400)