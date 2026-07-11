import json
import redis

from app.core.config import settings


class RedisClient:

    _client = None

    @classmethod
    def connect(cls):

        if cls._client is not None:
            return

        try:

            cls._client = redis.Redis(

                host=settings.REDIS_HOST,

                port=settings.REDIS_PORT,

                db=settings.REDIS_DB,

                password=settings.REDIS_PASSWORD or None,

                decode_responses=True

            )

            cls._client.ping()

            print("✅ Redis Connected")

        except Exception as e:

            cls._client = None

            print(f"❌ Redis Connection Failed : {e}")

    @classmethod
    def disconnect(cls):

        if cls._client is not None:

            cls._client.close()

            cls._client = None

            print("✅ Redis Closed")

    @classmethod
    def is_connected(cls):

        return cls._client is not None

    @classmethod
    def exists(
        cls,
        key: str
    ):

        if cls._client is None:
            return False

        return bool(
            cls._client.exists(key)
        )

    @classmethod
    def delete(
        cls,
        key: str
    ):

        if cls._client is None:
            return

        cls._client.delete(key)

    @classmethod
    def clear(cls):

        if cls._client is None:
            return

        cls._client.flushdb()

    @classmethod
    def set_json(

        cls,

        key: str,

        value,

        ttl: int = 300

    ):

        if cls._client is None:
            return

        cls._client.setex(

            key,

            ttl,

            json.dumps(value)

        )

    @classmethod
    def get_json(

        cls,

        key: str

    ):

        if cls._client is None:
            return None

        value = cls._client.get(key)

        if value is None:
            return None

        return json.loads(value)

    @classmethod
    def total_keys(cls):

        if cls._client is None:
            return 0

        return len(
            cls._client.keys("*")
        )