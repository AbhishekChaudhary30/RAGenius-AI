from app.cache.redis_client import RedisClient


class CacheService:

    DEFAULT_TTL = 300

    EMBEDDING_TTL = 3600

    @classmethod
    def get(

        cls,

        key: str

    ):

        return RedisClient.get_json(
            key
        )

    @classmethod
    def set(

        cls,

        key: str,

        value,

        ttl: int | None = None

    ):

        RedisClient.set_json(

            key,

            value,

            ttl or cls.DEFAULT_TTL

        )

    @classmethod
    def delete(

        cls,

        key: str

    ):

        RedisClient.delete(
            key
        )

    @classmethod
    def clear(cls):

        RedisClient.clear()

    @classmethod
    def exists(

        cls,

        key: str

    ):

        return RedisClient.exists(
            key
        )

    @classmethod
    def total_keys(cls):

        return RedisClient.total_keys()