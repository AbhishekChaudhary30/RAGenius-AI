class SessionManager:

    _sessions = {}

    @classmethod
    def create_session(cls):
        import uuid

        session_id = str(uuid.uuid4())
        cls._sessions[session_id] = []

        return session_id

    @classmethod
    def get_or_create(
        cls,
        session_id: str | None
    ):

        if session_id is None:
            return cls.create_session()

        if session_id not in cls._sessions:
            cls._sessions[session_id] = []

        return session_id