"""The bot's settings, read once from the environment at start-up."""

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import AnyHttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Every setting the bot reads. Names match the environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    discord_token: SecretStr
    trivia_service_url: AnyHttpUrl
    trivia_service_api_key: SecretStr
    database_url: str = "sqlite+aiosqlite:////data/trivia_bot.db"
    ops_guild_id: int | None = None
    ops_channel_id: int | None = None
    timezone: str = "UTC"
    sync_commands: bool = False
    log_level: str = "INFO"

    @field_validator("timezone")
    @classmethod
    def _known_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError) as error:
            raise ValueError(f"unknown time zone {value!r}") from error
        return value

    @field_validator("log_level")
    @classmethod
    def _known_log_level(cls, value: str) -> str:
        level = value.upper()
        if level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError(f"unknown log level {value!r}")
        return level
