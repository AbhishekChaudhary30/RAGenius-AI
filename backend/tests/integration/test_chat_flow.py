from app.memory.session_manager import SessionManager


def test_session_creation():

    session = SessionManager.get_or_create(
        None
    )

    assert session is not None