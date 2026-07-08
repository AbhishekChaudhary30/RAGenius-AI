from app.services.embedding_service import EmbeddingService
from app.vectordb.chroma_service import ChromaService


class SearchService:

    @staticmethod
    def semantic_search(
        query: str,
        top_k: int = 5
    ):

        embedding = EmbeddingService.embed_text(query)

        results = ChromaService.search(
            embedding,
            top_k
        )

        return results