from app.vectordb.chroma_service import ChromaService


class KeywordSearchService:

    @staticmethod
    def search(
        query: str,
        top_k: int = 5
    ):

        collection = ChromaService.get_collection()

        data = collection.get(
            limit=500,
            include = [
                "documents",
                "metadatas"
            ]
        )

        query_words = query.lower().split()

        results = []

        documents = data.get(
            "documents",
            []
        )

        metadatas = data.get(
            "metadatas",
            []
        )

        for document, metadata in zip(
            documents,
            metadatas
        ):

            text = document.lower()

            score = sum(

                word in text

                for word in query_words

            )

            if score > 0:

                results.append({

                    "text": document,

                    "filename": metadata.get(
                        "filename"
                    ),

                    "chunk_index": metadata.get(
                        "chunk_index"
                    ),

                    "keyword_score": score

                })

        results.sort(

            key=lambda x: x["keyword_score"],

            reverse=True

        )

        return results[:top_k]