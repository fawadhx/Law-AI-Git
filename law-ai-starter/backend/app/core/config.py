from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Law AI Backend"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    openai_api_key: str | None = None
    database_url: str | None = None
    database_echo: bool = False
    database_pool_pre_ping: bool = True
    database_auto_create_tables: bool = False
    database_bootstrap_legal_sources: bool = False
    database_bootstrap_force_refresh: bool = False
    legal_source_embedding_dimensions: int = 1536
    redis_url: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value):
        if isinstance(value, str):
            cleaned = value.strip()

            if cleaned.startswith("[") and cleaned.endswith("]"):
                cleaned = cleaned[1:-1]

            parts = [item.strip().strip('"').strip("'") for item in cleaned.split(",")]
            return [item for item in parts if item]

        return value


settings = Settings()
