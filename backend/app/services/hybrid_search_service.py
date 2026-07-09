from app.services.search_service import SearchService
from app.services.keyword_search_service import KeywordSearchService

import logging

logger = logging.getLogger(__name__)

class HybridSearchService:

    VECTOR_WEIGHT = 0.7
    KEYWORD_WEIGHT = 0.3

    @classmethod
    def search(
        cls,
        query: str,
        top_k: int = 5
    ):

        vector_results = SearchService.search(
            query=query,
            top_k=min(top_k, 10)
        )

        keyword_results = KeywordSearchService.search(
            query=query,
            top_k=min(top_k, 10)
        )

        merged = {}

        for result in vector_results:

            key = (
                result["filename"],
                result["chunk_index"]
            )

            result["hybrid_score"] = (
                result["score"] *
                cls.VECTOR_WEIGHT
            )

            merged[key] = result

        for result in keyword_results:

            key = (
                result["filename"],
                result["chunk_index"]
            )

            keyword_score = (
                result["keyword_score"] *
                cls.KEYWORD_WEIGHT
            )

            if key in merged:

                merged[key]["hybrid_score"] += keyword_score

            else:

                result["hybrid_score"] = keyword_score

                merged[key] = result

        results = list(
            merged.values()
        )

        results.sort(
            key=lambda x: x["hybrid_score"],
            reverse=True
        )

        filtered = []
        for item in results:
            if item["hybrid_score"] >= 0.20:
                filtered.append(item)
                
        logger.info(
            f"Hybrid Search | Query = {query} | Results = {len(filtered)}"
        )

        return filtered[:top_k]