from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Config(BaseSettings):
    GROQ_API_KEY: str
    GEMINI_API_KEY: str 

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Config()