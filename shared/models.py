from shared.config import settings
class GroqLLMModel:
    def __init__(self):  
        self.groq_llm = None

    def groq_chat(self):
        if self.groq_llm is None:
            from langchain_groq import ChatGroq

            self.groq_llm = ChatGroq(
                model=settings.MODEL_NAME,
                api_key=settings.GROQ_API_KEY,
            )

        return self.groq_llm

    def invoke(self, prompt):
        return self.groq_chat().invoke(prompt)

if __name__ == "__main__":
    model = GroqLLMModel()
    response=model.invoke("Bạn nói tiếng Việt được không?")
    print(response.content)