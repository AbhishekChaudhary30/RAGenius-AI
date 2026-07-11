from app.services.rag_service import RAGService


def test_rag_service_exists():

    assert hasattr(
        RAGService,
        "ask"
    )

    assert hasattr(
        RAGService,
        "stream"
    )

    assert hasattr(
        RAGService,
        "stream_events"
    )