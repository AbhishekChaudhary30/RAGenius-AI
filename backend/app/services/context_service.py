class ContextService:

    MAX_CONTEXT_LENGTH = 12000

    @classmethod
    def build_context(
        cls,
        search_results
    ):

        if not search_results:
            return ""

        context = []

        current_length = 0

        for item in search_results:

            text = item["text"].strip()

            if not text:
                continue

            if current_length + len(text) > cls.MAX_CONTEXT_LENGTH:
                break

            context.append(
                f"[Source: {item['filename']} | Chunk: {item['chunk_index']}]\n{text}"
            )

            current_length += len(text)

        return "\n\n".join(context)