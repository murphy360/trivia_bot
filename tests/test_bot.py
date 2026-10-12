"""Start-up: intents, the command tree and command sync."""

import asyncio
from unittest.mock import AsyncMock, MagicMock

from trivia_bot.admin import sync_commands
from trivia_bot.bot import TriviaBot, bot_intents
from trivia_bot.config import Settings


def make_bot(sync: bool) -> TriviaBot:
    settings = Settings(
        discord_token="t",
        trivia_service_url="http://trivia_service:8000",
        trivia_service_api_key="k",
        sync_commands=sync,
    )
    bot = TriviaBot(settings)
    bot.tree.sync = AsyncMock(return_value=[])
    return bot


def test_intents_are_servers_and_members_only():
    intents = bot_intents()
    assert intents.guilds
    assert intents.members
    assert not intents.presences
    assert not intents.message_content
    assert not intents.guild_messages


def test_start_up_does_not_sync_by_default(env):
    bot = make_bot(sync=False)
    asyncio.run(bot.setup_hook())
    bot.tree.sync.assert_not_awaited()
    assert bot.tree.get_command("admin") is not None


def test_start_up_syncs_when_asked(env):
    bot = make_bot(sync=True)
    asyncio.run(bot.setup_hook())
    bot.tree.sync.assert_awaited_once()


def fake_interaction() -> MagicMock:
    interaction = MagicMock()
    interaction.response.send_message = AsyncMock()
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()
    return interaction


def fake_bot(owner: bool) -> MagicMock:
    bot = MagicMock()
    bot.is_owner = AsyncMock(return_value=owner)
    bot.tree.sync = AsyncMock(return_value=["trivia", "admin"])
    return bot


def test_admin_sync_refuses_non_owner():
    bot, interaction = fake_bot(owner=False), fake_interaction()
    asyncio.run(sync_commands(bot, interaction))
    bot.tree.sync.assert_not_awaited()
    message = interaction.response.send_message.await_args
    assert "owner" in message.args[0]
    assert message.kwargs["ephemeral"] is True


def test_admin_sync_for_owner():
    bot, interaction = fake_bot(owner=True), fake_interaction()
    asyncio.run(sync_commands(bot, interaction))
    bot.tree.sync.assert_awaited_once()
    interaction.response.defer.assert_awaited_once()
    reply = interaction.followup.send.await_args
    assert reply.args[0] == "Synced 2 commands."
    assert reply.kwargs["ephemeral"] is True
