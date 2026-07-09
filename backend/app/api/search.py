from typing import Optional

from fastapi import APIRouter, HTTPException

from app.services.hybrid_search_service import HybridSearchService

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("/")
def hybrid_search(
    query: str,
    top_k: int = 5,
    filename: Optional[str] = None
):

    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    if top_k < 1 or top_k > 20:
        raise HTTPException(
            status_code=400,
            detail="top_k must be between 1 and 20."
        )

    results = HybridSearchService.search(
        query=query,
        top_k=top_k
    )

    if filename:
        results = [
            item
            for item in results
            if item["filename"] == filename
        ]

    return {

        "query": query,

        "search_type": "Hybrid Search",

        "total_results": len(results),

        "results": results

    }