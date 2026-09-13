from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "B2B Indic Support Bot"
    mongodb_url: str
    mongodb_database: str = "b2b_support_bot"
    redis_url: str
    model_provider: str = "ollama"
    model_base_url: str = "http://127.0.0.1:11434/v1"
    model_chat_model: str = "qwen2.5:3b"
    model_api_key: str = "ollama"
    rag_data_path: str = "../rag-data"
    whatsapp_bridge_secret: str = ""
    host: str = "0.0.0.0"
    port: int = 8000

settings = Settings()
