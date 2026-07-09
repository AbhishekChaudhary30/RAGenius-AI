class PromptBuilder:

    @staticmethod
    def build(

        question: str,

        context: str

    ):

        return f"""
You are an AI Assistant.

Answer ONLY using the provided context.

If the answer is not present,
reply:

'I could not find the answer in the uploaded documents.'

Context:

{context}

Question:

{question}
"""