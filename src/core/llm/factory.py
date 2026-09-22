from .interface import ILLMService
from .providers import GeminiService, GPTService, GroqService

class LLMFactory:
    @staticmethod
    def get_llm_service(provider: str) -> ILLMService:
        if provider == "gemini":
            return GeminiService()
        elif provider == "openai":
            return GPTService()
        elif provider == "groq":
            return GroqService()
        else:
            raise ValueError(f"Provider {provider} não suportado")
    