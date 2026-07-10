import time


class MetricsService:

    @staticmethod
    def now():

        return time.perf_counter()

    @staticmethod
    def elapsed(

        start: float

    ) -> float:

        return round(

            time.perf_counter() - start,

            4

        )

    @staticmethod
    def build_metrics(

        retrieval_time: float,

        generation_time: float,

        total_time: float,

        context_length: int,

        history_length: int,

        total_sources: int,

        provider: str

    ):

        return {

            "retrieval_time_sec": retrieval_time,

            "generation_time_sec": generation_time,

            "total_time_sec": total_time,

            "context_length": context_length,

            "history_length": history_length,

            "total_sources": total_sources,

            "provider": provider

        }
        
    _requests = []

    MAX_REQUESTS = 1000

    @classmethod
    def record(

        cls,

        metrics: dict

    ):

        cls._requests.append(
            metrics
        )

        if len(cls._requests) > cls.MAX_REQUESTS:

            cls._requests = (

                cls._requests[-cls.MAX_REQUESTS:]

            )

    @classmethod
    def all_metrics(cls):

        return cls._requests

    @classmethod
    def statistics(cls):

        total = len(cls._requests)

        if total == 0:

            return {

                "total_requests": 0,

                "average_retrieval_time": 0,

                "average_generation_time": 0,

                "average_total_time": 0,

                "average_context_length": 0,

                "average_history_length": 0,

                "average_sources": 0,

                "slowest_request": 0,

                "fastest_request": 0,

                "providers": {}

            }

        retrieval_sum = 0

        generation_sum = 0

        total_sum = 0

        context_sum = 0

        history_sum = 0

        source_sum = 0

        providers = {}

        slowest = 0

        fastest = None

        for item in cls._requests:

            retrieval_sum += item["retrieval_time_sec"]

            generation_sum += item["generation_time_sec"]

            total_sum += item["total_time_sec"]

            context_sum += item["context_length"]

            history_sum += item["history_length"]

            source_sum += item["total_sources"]

            provider = item["provider"]

            providers[provider] = (

                providers.get(

                    provider,

                    0

                ) + 1

            )

            if item["total_time_sec"] > slowest:

                slowest = item["total_time_sec"]

            if (

                fastest is None

                or

                item["total_time_sec"] < fastest

            ):

                fastest = item["total_time_sec"]

        return {

            "total_requests": total,

            "average_retrieval_time":

                round(

                    retrieval_sum / total,

                    4

                ),

            "average_generation_time":

                round(

                    generation_sum / total,

                    4

                ),

            "average_total_time":

                round(

                    total_sum / total,

                    4

                ),

            "average_context_length":

                round(

                    context_sum / total,

                    2

                ),

            "average_history_length":

                round(

                    history_sum / total,

                    2

                ),

            "average_sources":

                round(

                    source_sum / total,

                    2

                ),

            "slowest_request":

                slowest,

            "fastest_request":

                fastest,

            "providers":

                providers

        }