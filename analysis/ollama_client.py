import ollama


class OllamaClient:

    def __init__(self, model="gemma4:latest"): #you can change the model in here..tested with DeepSeek model,qwen3:8b model available in Ollama
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