from abc import ABC, abstractmethod
from bear.domain.models import AudioPayload

class IAudioRecorder(ABC):
    @abstractmethod
    def record_audio(self) -> AudioPayload | None:
        pass