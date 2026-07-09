from app.services.hybrid_search_service import HybridSearchService

from app.services.context_service import ContextService

from app.llm.prompt_builder import PromptBuilder

from app.llm.provider_factory import ProviderFactory


class RAGService:

    @staticmethod
    def ask(
        question: str,
        top_k: int = 5
    ):

        search_results = HybridSearchService.search(
            query=question,
            top_k=top_k
        )

        context = ContextService.build_context(
            search_results
        )

        prompt = PromptBuilder.build(
            question=question,
            context=context
        )

        provider = ProviderFactory.get_provider()

        answer = provider.generate(
            prompt
        )

        return {

            "question": question,

            "answer": answer,

            "sources": search_results

        }