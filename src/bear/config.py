from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from pathlib import Path
from bear.domain.models import LanguageProfile

root = Path(__file__).resolve().parents[2]

LANGUAGE_PROFILES: dict[str, LanguageProfile] = {
        "en": LanguageProfile(
            stt_language="en",
            stt_prompt="The audio is in english",
            tts_voice="en-US-ChristopherNeural",
            llm_instruction="conversational plain-text English.",
        ),
        "pt": LanguageProfile(
            stt_language="pt",
            stt_prompt="O audio esta em portugues",
            tts_voice="pt-BR-AntonioNeural",
            llm_instruction="conversational plain-text Brazilian potuguese.",
        ),
    }


class Config(BaseSettings):
    GROQ_API_KEY: str
    GEMINI_API_KEY: str 
    OPENAI_API_KEY: str | None = None
    GNEWS_API_KEY: str
    EXCHANGERATE_API_KEY: str
    LLM_PROVIDER: Literal["gemini", "openai", "groq"]
    WEATHER_API_KEY: str
    MODEL_PATH: Path = root / "models" / "Hey_Jarvis.onnx"
    LANGUAGE: Literal["en", "pt"] = "pt"
    SPOTIPY_CLIENT_ID: str
    SPOTIPY_CLIENT_SECRET: str
    SPOTIPY_REDIRECT_URI: str = "http://127.0.0.1:8888/callback"
    FAVORITE_DEVICE: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def profile(self) -> LanguageProfile:
        return LANGUAGE_PROFILES[self.LANGUAGE]

config = Config()