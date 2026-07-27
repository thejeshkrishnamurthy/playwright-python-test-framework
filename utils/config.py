from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ui_base_url: str = "https://www.saucedemo.com"
    api_base_url: str = "https://restful-booker.herokuapp.com"

    standard_user: str = "standard_user"
    standard_password: str = "secret_sauce"

    api_username: str = "admin"
    api_password: str = "password123"

    default_timeout_ms: int = 10_000
    headless: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
