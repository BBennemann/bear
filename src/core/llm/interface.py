from abc import ABC, abstractmethod

class ILLMService(ABC):
    @abstractmethod
    def enviar_pergunta(self, pergunta: str) -> str:
        pass