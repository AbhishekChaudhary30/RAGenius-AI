class ContextService:

    @staticmethod
    def build_context(

        search_results

    ):

        context = []

        for item in search_results:

            context.append(
                item["text"]
            )

        return "\n\n".join(
            context
        )