import chromadb
from chromadb.config import Settings


class ChromaService:

    _client = None
    _collection = None

    @classmethod
    def get_collection(cls):

        if cls._collection is None:

            cls._client = chromadb.PersistentClient(
                path="chroma_db",
                settings=Settings(
                    anonymized_telemetry=False
                )
            )

            cls._collection = cls._client.get_or_create_collection(
                name="documents"
            )

        return cls._collection

    @classmethod
    def store_chunks(
        cls,
        filename: str,
        chunks
    ):

        collection = cls.get_collection()

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for index, chunk in enumerate(chunks):

            ids.append(f"{filename}_{index}")

            documents.append(chunk.text)

            embeddings.append(chunk.embedding)

            metadatas.append({
                "filename": filename,
                "chunk_index": index
            })

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    @classmethod
    def search(
        cls,
        query_embedding,
        top_k: int = 5
    ):

        collection = cls.get_collection()

        return collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )