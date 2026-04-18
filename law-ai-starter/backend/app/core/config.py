from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Law AI Backend"
    app_version: str = "0.1.0"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_public_base_url: str | None = None
    app_log_level: str = "INFO"
    app_log_json: bool = False
    app_request_logging_enabled: bool = True
    app_readiness_requires_database: bool = False
    app_readiness_requires_openai: bool = False
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    openai_api_key: str | None = None
    database_url: str | None = None
    database_echo: bool = False
    database_pool_pre_ping: bool = True
    database_pool_size: int = 5
    database_max_overflow: int = 10
    database_connect_timeout_seconds: int = 5
    database_auto_create_tables: bool = False
    database_bootstrap_legal_sources: bool = False
    database_bootstrap_force_refresh: bool = False
    legal_source_embedding_dimensions: int = 1536
    legal_source_embedding_model: str = "text-embedding-3-small"
    legal_source_vector_search_enabled: bool = False
    legal_source_vector_query_top_k: int = 8
    redis_url: str | None = None
    admin_auth_secret_key: str = "change-this-law-ai-admin-secret"
    admin_auth_issuer: str = "law-ai-admin"
    admin_auth_username: str = "admin"
    admin_auth_display_name: str = "Admin"
    admin_auth_role: str = "admin"
    admin_auth_password: str = "admin123"
    admin_auth_password_sha256: str | None = None
    admin_auth_access_token_ttl_minutes: int = 480
    admin_auth_write_roles: list[str] = ["admin"]

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

    @field_validator("admin_auth_write_roles", mode="before")
    @classmethod
    def parse_admin_write_roles(cls, value):
        if isinstance(value, str):
            cleaned = value.strip()

            if cleaned.startswith("[") and cleaned.endswith("]"):
                cleaned = cleaned[1:-1]

            parts = [item.strip().strip('"').strip("'") for item in cleaned.split(",")]
            return [item for item in parts if item]

        return value

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    @property
    def admin_auth_uses_default_secret(self) -> bool:
        return self.admin_auth_secret_key == "change-this-law-ai-admin-secret"

    @property
    def admin_auth_uses_default_password(self) -> bool:
        return self.admin_auth_password == "admin123" and not self.admin_auth_password_sha256

    def runtime_warnings(self) -> list[str]:
        warnings: list[str] = []

        if self.is_production and self.admin_auth_uses_default_secret:
            warnings.append("Admin auth is still using the default secret key.")
        if self.is_production and self.admin_auth_uses_default_password:
            warnings.append("Admin auth is still using the default password.")
        if not self.allowed_origins:
            warnings.append("No frontend origins are configured in ALLOWED_ORIGINS.")
        if self.app_readiness_requires_openai and not self.openai_api_key:
            warnings.append("OpenAI readiness is required but OPENAI_API_KEY is not configured.")

        return warnings


settings = Settings()
