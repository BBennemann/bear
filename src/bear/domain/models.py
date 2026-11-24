from dataclasses import dataclass

@dataclass(frozen = True)
class AudioPayload():
    data: bytes
    filename: str = "audio.wav"

@dataclass(frozen = True)
class LanguageProfile():
    stt_language: str
    stt_prompt: str
    tts_voice: str
    llm_instruction: str