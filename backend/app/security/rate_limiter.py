from collections import defaultdict
from datetime import datetime, timedelta


class RateLimiter:

    REQUEST_LIMIT = 60

    WINDOW_SECONDS = 60

    _requests = defaultdict(list)

    @classmethod
    def allow_request(
        cls,
        client_id: str
    ) -> bool:

        now = datetime.utcnow()

        window_start = now - timedelta(
            seconds=cls.WINDOW_SECONDS
        )

        cls._requests[client_id] = [

            timestamp

            for timestamp in cls._requests[client_id]

            if timestamp > window_start

        ]

        if len(cls._requests[client_id]) >= cls.REQUEST_LIMIT:

            return False

        cls._requests[client_id].append(now)

        return True