from groq import Groq
from bear.domain.models import AudioPayload
from bear.domain.exceptions import TranscriptionError
from bear.domain.interfaces.stt_service import ISTTService

class GroqWhisperSTT(ISTTService):

    def __init__(self, api_key: str, language: str, prompt: str):
        self.client = Groq(api_key=api_key)
        self.language = language
        self.prompt = prompt

    def transcribe(self, audio: AudioPayload) -> str:
        try: 
            return self.client.audio.transcriptions.create(
                file=(audio.filename, audio.data),
                model="whisper-large-v3", # The most accurate model
                prompt=self.prompt, # Optional context helps with accuracy
                response_format="text",
                language=self.language # Force English
            )
        except Exception as e:
            raise TranscriptionError(f"Failed to transcribe audio: {e}") from e