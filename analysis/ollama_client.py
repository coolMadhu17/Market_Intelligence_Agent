import ollama


class OllamaClient:

    def __init__(self, model="gemma4:latest"):
        self.model = model

    def ask(self, prompt):

        try:
            response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        except Exception as e:
            print(e)
            raise
        return response["message"]["content"]