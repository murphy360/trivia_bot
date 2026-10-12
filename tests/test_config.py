"""Settings: required values, defaults and bad values."""

import logging
from unittest.mock import MagicMock

import discord
import pytest
from pydantic import ValidationError

from trivia_bot.__main__ import load_settings, main
from trivia_bot.bot import TriviaBot
from trivia_bot.config import Settings


def test_required_values_missing(clean_env):
    with pytest.raises(ValidationError) as caught:
        Settings()
    missing = {problem["loc"][0] for problem in caught.value.errors()}
    assert missing == {"discord_token", "trivia_service_url", "trivia_service_api_key"}


def test_defaults_applied(env):
    settings = Settings()
    assert settings.database_url == "sqlite+aiosqlite:////data/trivia_bot.db"
    assert settings.ops_guild_id is None
    assert settings.ops_channel_id is None
    assert settings.timezone == "UTC"
    assert settings.sync_commands is False
    assert settings.log_level == "INFO"


def test_secrets_are_hidden(env):
    settings = Settings()
    assert "test-token" not in repr(settings)
    assert settings.discord_token.get_secret_value() == "test-token"


def test_values_read_from_environment(env):
    env.setenv("TIMEZONE", "America/New_York")
    env.setenv("SYNC_COMMANDS", "true")
    env.setenv("OPS_CHANNEL_ID", "1234")
    env.setenv("LOG_LEVEL", "debug")
    settings = Settings()
    assert settings.timezone == "America/New_York"
    assert settings.sync_commands is True
    assert settings.ops_channel_id == 1234
    assert settings.log_level == "DEBUG"


def test_values_read_from_env_file(clean_env, tmp_path):
    (tmp_path / ".env").write_text(
        "DISCORD_TOKEN=file-token\n"
        "TRIVIA_SERVICE_URL=http://localhost:8000\n"
        "TRIVIA_SERVICE_API_KEY=file-key\n"
    )
    assert Settings().discord_token.get_secret_value() == "file-token"


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("TIMEZONE", "Mars/Olympus_Mons"),
        ("LOG_LEVEL", "LOUD"),
        ("TRIVIA_SERVICE_URL", "not a url"),
        ("OPS_CHANNEL_ID", "general"),
    ],
)
def test_bad_value_rejected(env, name, value):
    env.setenv(name, value)
    with pytest.raises(ValidationError):
        Settings()


def test_load_settings_exits_with_one_line_per_problem(clean_env, caplog):
    with caplog.at_level(logging.ERROR), pytest.raises(SystemExit) as caught:
        load_settings()
    assert caught.value.code == 2
    lines = [record.getMessage() for record in caplog.records]
    assert len(lines) == 3
    assert any(line.startswith("setting DISCORD_TOKEN:") for line in lines)


@pytest.mark.parametrize(
    ("error", "expected"),
    [
        (discord.LoginFailure("bad"), "refused the token"),
        (discord.PrivilegedIntentsRequired(None), "Server Members Intent"),
    ],
)
def test_start_up_failure_is_one_line(env, monkeypatch, caplog, error, expected):
    monkeypatch.setattr(TriviaBot, "run", MagicMock(side_effect=error))
    with caplog.at_level(logging.ERROR), pytest.raises(SystemExit) as caught:
        main()
    assert caught.value.code == 2
    assert expected in caplog.records[-1].getMessage()
