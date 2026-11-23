from abc import ABC, abstractmethod
from bear.domain.models import AudioPayload

class ISTTService(ABC):

    @abstractmethod
    def transcribe(self, audio: AudioPayload) -> str:
        pass