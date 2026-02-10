from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Config(BaseSettings):
    GROQ_API_KEY: str
    GEMINI_API_KEY: str 
    OPENAI_API_KEY: str | None = None
    PICOVOICE_API_KEY: str
    LLM_PROVIDER: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Config()