from app.services.hybrid_search_service import HybridSearchService
from app.services.context_service import ContextService

from app.llm.prompt_builder import PromptBuilder
from app.llm.provider_factory import ProviderFactory

from app.memory.memory_service import MemoryService
from app.memory.session_manager import SessionManager

from app.services.memory_summary_service import (
    MemorySummaryService
)


class RAGService:

    @staticmethod
    def ask(
        question: str,
        top_k: int = 5,
        session_id: str | None = None
    ):

        session_id = SessionManager.get_or_create(
            session_id
        )

        search_results = HybridSearchService.search(
            query=question,
            top_k=top_k
        )

        if len(search_results) == 0:

            return {

                "session_id": session_id,

                "question": question,

                "answer": "I could not find the answer in the uploaded documents.",

                "sources": [],

                "total_sources": 0,

                "history_messages": MemoryService.total_messages(
                    session_id
                )

            }

        context = ContextService.build_context(
            search_results
        )

        history = MemoryService.build_history(
            session_id
        )

        provider = ProviderFactory.get_provider()

        if MemorySummaryService.should_summarize(
            session_id
        ):

            summary_prompt = (

                MemorySummaryService.build_summary_prompt(
                    session_id
                )

            )

            summary = provider.generate(
                summary_prompt
            )

            MemorySummaryService.finalize_summary(
                session_id,
                summary
            )

            history = MemoryService.build_history(
                session_id
            )

        prompt = PromptBuilder.build(

            question=question,

            context=context,

            history=history

        )

        answer = provider.generate(
            prompt
        )

        MemoryService.add_message(

            session_id,

            "User",

            question

        )
        
        SessionManager.increment_messages(
            session_id
        )

        MemoryService.add_message(

            session_id,

            "Assistant",

            answer

        )
        
        SessionManager.increment_messages(
            session_id
        )

        history_message_count = MemoryService.total_messages(
            session_id
        )

        sources = []

        for item in search_results:

            source = {

                "filename": item["filename"],

                "chunk_index": item["chunk_index"]

            }

            if source not in sources:

                sources.append(source)

        return {

            "session_id": session_id,

            "question": question,

            "answer": answer,

            "sources": sources,

            "total_sources": len(sources),

            "history_messages": history_message_count

        }
        
    @staticmethod
    def stream(
        question: str,
        top_k: int = 5,
        session_id: str | None = None
    ):

        session_id = SessionManager.get_or_create(
            session_id
        )

        search_results = HybridSearchService.search(
            query=question,
            top_k=top_k
        )

        if len(search_results) == 0:

            yield (
                "I could not find the answer "
                "in the uploaded documents."
            )

            return

        context = ContextService.build_context(
            search_results
        )

        history = MemoryService.build_history(
            session_id
        )

        provider = ProviderFactory.get_provider()

        if MemorySummaryService.should_summarize(
            session_id
        ):

            summary_prompt = (
                MemorySummaryService.build_summary_prompt(
                    session_id
                )
            )

            summary = provider.generate(
                summary_prompt
            )

            MemorySummaryService.finalize_summary(
                session_id,
                summary
            )

            history = MemoryService.build_history(
                session_id
            )

        prompt = PromptBuilder.build(

            question=question,

            context=context,

            history=history

        )

        MemoryService.add_message(

            session_id,

            "User",

            question

        )
        
        SessionManager.increment_messages(
            session_id
        )

        complete_answer = ""

        for token in provider.generate_stream(
            prompt
        ):

            complete_answer += token

            yield token

        MemoryService.add_message(

            session_id,

            "Assistant",

            complete_answer

        )
        
        SessionManager.increment_messages(
            session_id
        )
        
    @staticmethod
    def stream_events(
        question: str,
        top_k: int = 5,
        session_id: str | None = None
    ):

        session_id = SessionManager.get_or_create(
            session_id
        )

        yield {
            "event": "session",
            "data": session_id
        }

        search_results = HybridSearchService.search(
            query=question,
            top_k=top_k
        )

        if len(search_results) == 0:

            yield {
                "event": "error",
                "data": "I could not find the answer in the uploaded documents."
            }

            yield {
                "event": "done",
                "data": ""
            }

            return

        context = ContextService.build_context(
            search_results
        )

        history = MemoryService.build_history(
            session_id
        )

        provider = ProviderFactory.get_provider()

        if MemorySummaryService.should_summarize(
            session_id
        ):

            summary_prompt = (
                MemorySummaryService.build_summary_prompt(
                    session_id
                )
            )

            summary = provider.generate(
                summary_prompt
            )

            MemorySummaryService.finalize_summary(
                session_id,
                summary
            )

            history = MemoryService.build_history(
                session_id
            )

        prompt = PromptBuilder.build(
            question=question,
            context=context,
            history=history
        )

        MemoryService.add_message(
            session_id,
            "User",
            question
        )
        
        SessionManager.increment_messages(
            session_id
        )

        answer = ""

        for token in provider.generate_stream(
            prompt
        ):

            answer += token

            yield {
                "event": "token",
                "data": token
            }

        MemoryService.add_message(
            session_id,
            "Assistant",
            answer
        )
        
        SessionManager.increment_messages(
            session_id
        )

        sources = []

        for item in search_results:

            source = {

                "filename": item["filename"],

                "chunk_index": item["chunk_index"]

            }

            if source not in sources:

                sources.append(source)

        yield {
            "event": "sources",
            "data": sources
        }

        yield {
            "event": "done",
            "data": ""
        }