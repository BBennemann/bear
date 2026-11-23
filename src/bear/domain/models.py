from dataclasses import dataclass

@dataclass(frozen = True)
class AudioPayload():
    data: bytes
    filename: str = "audio.wav"