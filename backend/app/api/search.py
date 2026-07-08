from typing import Optional

from fastapi import APIRouter, HTTPException

from app.services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("/")
def semantic_search(
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

    results = SearchService.search(
        query=query,
        top_k=top_k
    )

    if filename:
        results = [
            result
            for result in results
            if result["filename"] == filename
        ]

    return {
        "query": query,
        "top_k": top_k,
        "total_results": len(results),
        "results": results
    }