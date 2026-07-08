from fastapi import APIRouter

from app.services.embedding_service import EmbeddingService

router = APIRouter(
    prefix="/embeddings",
    tags=["Embeddings"]
)


@router.get("/test")
def test_embedding():

    text = "Artificial Intelligence is transforming the world."

    embedding = EmbeddingService.embed_text(text)

    return {

        "text": text,

        "embedding_dimension": len(embedding),

        "first_10_values": embedding[:10]

    }