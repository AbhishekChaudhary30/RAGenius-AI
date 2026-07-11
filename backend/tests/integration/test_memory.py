from app.memory.memory_service import MemoryService


def test_memory_history():

    session = "integration-session"

    MemoryService.clear_session(
        session
    )

    MemoryService.add_message(
        session,
        "User",
        "Hello"
    )

    MemoryService.add_message(
        session,
        "Assistant",
        "Hi"
    )

    history = MemoryService.build_history(
        session
    )

    assert "Hello" in history

    assert "Hi" in history