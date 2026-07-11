from app.cache.cache_keys import CacheKeys


def test_embedding_key():

    key = CacheKeys.embedding_key(
        "Hello"
    )

    assert key.startswith(
        "embedding:"
    )