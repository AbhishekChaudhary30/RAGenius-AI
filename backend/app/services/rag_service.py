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

        if len(search_results) == 0:

            return {

                "question": question,

                "answer": "I could not find the answer in the uploaded documents.",

                "sources": []

            }

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
        
        sources = []

        for item in search_results:

            source = {

                "filename": item["filename"],

                "chunk_index": item["chunk_index"]

            }

            if source not in sources:

                sources.append(source)

        return {
            "question": question,
            "answer": answer.strip(),
            "sources": sources,
            "total_sources": len(sources)

        }