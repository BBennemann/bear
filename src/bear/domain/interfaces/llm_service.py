from abc import ABC, abstractmethod

class ILLMService(ABC):
    @abstractmethod
    def send_query(self, query: str) -> str:
        pass