from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    GROQ_API_KEY: str
    GEMINI_API_KEY: str 
    OPENAI_API_KEY: str | None = None
    PICOVOICE_API_KEY: str
    GNEWS_API_KEY: str
    EXCHANGERATE_API_KEY: str
    LLM_PROVIDER: str
    WEATHER_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Config()