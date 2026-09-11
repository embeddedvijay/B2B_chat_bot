from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "B2B Indic Support Bot"
    database_url: str
    redis_url: str
    llm_provider: str = "openai"
    llm_chat_model: str = "gpt-5-mini"
    embedding_model: str = "text-embedding-3-large"
    openai_api_key: str = ""

settings = Settings()
