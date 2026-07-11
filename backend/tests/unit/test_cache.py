from app.cache.cache_keys import CacheKeys


def test_query_key():

    key = CacheKeys.query_key(
        "What is AI?",
        5
    )

    assert key.startswith(
        "rag:query:"
    )