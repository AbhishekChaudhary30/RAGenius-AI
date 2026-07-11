from app.services.hybrid_search_service import HybridSearchService
from app.services.context_service import ContextService

from app.llm.prompt_builder import PromptBuilder
from app.llm.provider_factory import ProviderFactory

from app.memory.memory_service import MemoryService
from app.memory.session_manager import SessionManager

from app.cache.redis_client import RedisClient
from app.cache.cache_keys import CacheKeys

from app.core.logging import logger

from app.services.memory_summary_service import (
    MemorySummaryService
)

from app.monitoring.metrics_service import (
    MetricsService
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
        
        cache_key = CacheKeys.query_key(
            question=question,
            top_k=top_k
        )

        cached_response = RedisClient.get_json(
            cache_key
        )

        if cached_response is not None:

            logger.info(
                "✅ Query Cache Hit"
            )

            cached_response["cached"] = True
            
            cached_response["session_id"] = session_id
            
            if "metrics" not in cached_response:
                cached_response["metrics"] = {
                    "retrieval_time_sec":0.0,
                    "generation_time_sec":0.0,
                    "total_time_sec":0.0,
                    "context_length":0,
                    "history_length":0,
                    "total_sources":
                        cached_response.get("total_sources",0),
                    "provider":"cache"
                }

            return cached_response
        
        total_start = MetricsService.now()
        
        retrieval_start = MetricsService.now()
        
        logger.info(
            "❌ Query Cache Miss"
        )

        search_results = HybridSearchService.search(
            query=question,
            top_k=top_k
        )
        
        retrieval_time = MetricsService.elapsed(
            retrieval_start
        )

        if len(search_results) == 0:

            response = {

                "session_id": session_id,

                "question": question,

                "answer": "I could not find the answer in the uploaded documents.",

                "sources": [],

                "total_sources": 0,

                "history_messages": MemoryService.total_messages(
                    session_id
                ),

                "metrics": {
                    "retrieval_time_sec": retrieval_time,
                    "generation_time_sec": 0.0,
                    "total_time_sec": MetricsService.elapsed(total_start),
                    "context_length": 0,
                    "history_length": 0,
                    "total_sources": 0,
                    "provider": "none"
                },

                "cached": False
            }

            RedisClient.set_json(
                key=cache_key,
                value=response,
                ttl=300
            )

            return response

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
        
        generation_start = MetricsService.now()

        answer = provider.generate(
            prompt
        )
        
        generation_time = MetricsService.elapsed(
            generation_start
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
        
        total_time = MetricsService.elapsed(
            total_start
        )
        
        sources = []
        
        for item in search_results:
            source = {
                "filename":item["filename"],
                "chunk_index":item["chunk_index"]
            }
            
            if source not in sources:
                sources.append(source)
                
        metrics = MetricsService.build_metrics(
            retrieval_time=retrieval_time,
            generation_time=generation_time,
            total_time=total_time,
            context_length=len(context),
            history_length=len(history),
            total_sources=len(sources),
            provider=type(provider).__name__
        )
        
        MetricsService.record(
            metrics
        )

        response = {
                "session_id":session_id,
                "question":question,
                "answer":answer,
                "sources":sources,
                "total_sources":len(sources),
                "history_messages":history_message_count,
                "metrics": metrics,
                "cached":False,
                "provider":type(provider).__name__
            }
            
        RedisClient.set_json(
            key=cache_key,
            value=response,
            ttl=300
        )
            
        return response
        
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
        
        total_start = MetricsService.now()

        yield {
            "event": "session",
            "data": session_id
        }
        
        retrieval_start = MetricsService.now()

        search_results = HybridSearchService.search(
            query=question,
            top_k=top_k
        )
        
        retrieval_time = MetricsService.elapsed(
            retrieval_start
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
        
        generation_start = MetricsService.now()

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
        
        generation_time = MetricsService.elapsed(
            generation_start
        )
        
        total_time = MetricsService.elapsed(
            total_start
        )
        
        metrics = MetricsService.build_metrics(
            retrieval_time=retrieval_time,
            generation_time=generation_time,
            total_time=total_time,
            context_length=len(context),
            history_length=len(history),
            total_sources=len(search_results),
            provider=type(provider).__name__
        )
        
        MetricsService.record(
            metrics
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
        
        yield{
            "event":"metrics",
            "data":metrics
        }

        yield {
            "event": "done",
            "data": ""
        }