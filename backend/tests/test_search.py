def test_vector_search_requires_query(client):

    response = client.get(
        "/api/v1/documents/search/vector"
    )

    assert response.status_code == 422