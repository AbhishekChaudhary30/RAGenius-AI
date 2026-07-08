from app.services.embedding_service import EmbeddingService
from app.vectordb.chroma_service import ChromaService


class SearchService:

    @staticmethod
    def search(
        query: str,
        top_k: int = 5
    ):

        try:

            query_embedding = EmbeddingService.embed_text(
                query
            )

            results = ChromaService.search(
                query_embedding=query_embedding,
                top_k=top_k
            )

            response = []

            documents = results.get(
                "documents",
                [[]]
            )[0]

            metadatas = results.get(
                "metadatas",
                [[]]
            )[0]

            distances = results.get(
                "distances",
                [[]]
            )[0]

            for document, metadata, distance in zip(

                documents,

                metadatas,

                distances

            ):

                response.append({

                    "text": document,

                    "filename": metadata.get(
                        "filename"
                    ),

                    "chunk_index": metadata.get(
                        "chunk_index"
                    ),

                    "score": round(
                        1 - distance,
                        4
                    )

                })

            response.sort(

                key=lambda x: x["score"],

                reverse=True

            )

            return response

        except Exception as e:

            raise RuntimeError(

                f"Vector Search Failed : {e}"

            )