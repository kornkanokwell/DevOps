from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """อ่านค่า config จาก environment variables (หรือไฟล์ .env)"""

    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 60
    environment: str = "development"
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def cors_origins_list(self) -> list[str]:
        # แปลง "url1,url2" → ["url1", "url2"]
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    # @lru_cache → อ่าน .env ครั้งเดียว แล้ว cache ไว้
    return Settings()  # type: ignore[call-arg]