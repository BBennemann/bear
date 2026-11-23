from abc import ABC, abstractmethod

class IWakeWord(ABC):

    @abstractmethod
    def listen_wake_word(self) -> None:
        pass

    @abstractmethod
    def terminate(self) -> None:
        pass