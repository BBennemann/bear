from .interface import ILLMService
from .providers import GeminiService, GPTService

class LLMFactory:
    @staticmethod
    def get_llm_service(provider: str) -> ILLMService:
        if provider == "gemini":
            return GeminiService()
        elif provider == "openai":
            return GPTService()
        else:
            raise ValueError(f"Provider {provider} não suportado")
    