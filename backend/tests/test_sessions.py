def test_list_sessions(client):

    response = client.get("/sessions/")

    assert response.status_code == 200


def test_clear_sessions(client):

    response = client.delete("/sessions/")

    assert response.status_code == 200