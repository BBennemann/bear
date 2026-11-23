from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from pathlib import Path

root = Path(__file__).resolve().parents[2]

class Config(BaseSettings):
    GROQ_API_KEY: str
    GEMINI_API_KEY: str 
    OPENAI_API_KEY: str | None = None
    GNEWS_API_KEY: str
    EXCHANGERATE_API_KEY: str
    LLM_PROVIDER: Literal["gemini", "openai", "groq"]
    WEATHER_API_KEY: str
    MODEL_PATH: Path = root / "models" / "Hey_Jarvis.onnx"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Config()