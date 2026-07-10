class MemoryService:

    MAX_MESSAGES = 10

    SUMMARY_TRIGGER = 8

    _memory = {}

    @classmethod
    def _create(cls, session_id: str):

        if session_id not in cls._memory:

            cls._memory[session_id] = {

                "summary": "",

                "messages": [],

                "summary_version": 0

            }

    @classmethod
    def add_message(

        cls,

        session_id: str,

        role: str,

        content: str

    ):

        cls._create(session_id)

        cls._memory[session_id]["messages"].append({

            "role": role,

            "content": content

        })

        if len(cls._memory[session_id]["messages"]) > cls.MAX_MESSAGES:

            cls._memory[session_id]["messages"] = (

                cls._memory[session_id]["messages"][-cls.MAX_MESSAGES:]

            )

    @classmethod
    def get_messages(

        cls,

        session_id: str

    ):

        cls._create(session_id)

        return cls._memory[session_id]["messages"]

    @classmethod
    def total_messages(

        cls,

        session_id: str

    ):

        return len(

            cls.get_messages(

                session_id

            )

        )

    @classmethod
    def build_history(

        cls,

        session_id: str

    ):

        cls._create(session_id)

        history = []

        summary = cls._memory[session_id]["summary"]

        if summary:

            history.append(

                f"Conversation Summary:\n{summary}"

            )

        for item in cls._memory[session_id]["messages"]:

            history.append(

                f"{item['role']}: {item['content']}"

            )

        return "\n".join(history)

    @classmethod
    def set_summary(

        cls,

        session_id: str,

        summary: str

    ):

        cls._create(session_id)

        cls._memory[session_id]["summary"] = summary.strip()

        cls._memory[session_id]["summary_version"] += 1

    @classmethod
    def trim_messages(

        cls,

        session_id: str,

        keep_last: int = 4

    ):

        cls._create(session_id)

        cls._memory[session_id]["messages"] = (

            cls._memory[session_id]["messages"][-keep_last:]

        )

    @classmethod
    def should_create_summary(

        cls,

        session_id: str

    ):

        cls._create(session_id)

        return (

            len(

                cls._memory[session_id]["messages"]

            ) >= cls.SUMMARY_TRIGGER

            and

            cls._memory[session_id]["summary_version"] == 0

        )

    @classmethod
    def clear_session(

        cls,

        session_id: str

    ):

        cls._memory.pop(

            session_id,

            None

        )
        
    @classmethod
    def get_session_data(

        cls,

        session_id: str

    ):

        cls._create(session_id)

        return cls._memory[session_id]

    @classmethod
    def session_exists(

        cls,

        session_id: str

    ):

        return session_id in cls._memory
    
    @classmethod
    def clear_all(

        cls

    ):

        cls._memory.clear()