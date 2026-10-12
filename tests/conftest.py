"""Shared fixtures: a clean environment with the required settings."""

import pytest

REQUIRED = {
    "DISCORD_TOKEN": "test-token",
    "TRIVIA_SERVICE_URL": "http://trivia_service:8000",
    "TRIVIA_SERVICE_API_KEY": "test-key",
}
OPTIONAL = [
    "DATABASE_URL",
    "OPS_GUILD_ID",
    "OPS_CHANNEL_ID",
    "TIMEZONE",
    "SYNC_COMMANDS",
    "LOG_LEVEL",
]


@pytest.fixture
def clean_env(monkeypatch, tmp_path):
    """No bot settings in the environment, and no .env file in the working dir."""
    monkeypatch.chdir(tmp_path)
    for name in [*REQUIRED, *OPTIONAL]:
        monkeypatch.delenv(name, raising=False)
    return monkeypatch


@pytest.fixture
def env(clean_env):
    """The required settings set, the optional ones left to their defaults."""
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)
    return clean_env
