from abc import ABC, abstractmethod

class ITTSService(ABC):

    @abstractmethod
    async def speak(self, text: str) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass