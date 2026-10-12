"""The Discord client: intents, start-up and the command tree."""

import logging

import discord
from discord.ext import commands

from trivia_bot.admin import admin_group
from trivia_bot.config import Settings

log = logging.getLogger(__name__)


def bot_intents() -> discord.Intents:
    """Servers and members only. No presences and no message content."""
    intents = discord.Intents.none()
    intents.guilds = True
    intents.members = True
    return intents


class TriviaBot(commands.Bot):
    """The bot. Slash commands only, so prefix commands answer to a mention."""

    def __init__(self, settings: Settings) -> None:
        super().__init__(command_prefix=commands.when_mentioned, intents=bot_intents())
        self.settings = settings

    async def setup_hook(self) -> None:
        self.tree.add_command(admin_group(self))
        if self.settings.sync_commands:
            synced = await self.tree.sync()
            log.info("commands synced at start-up: %d", len(synced))
        else:
            log.info("command sync skipped (SYNC_COMMANDS is off)")

    async def on_ready(self) -> None:
        log.info("ready as %s in %d servers", self.user, len(self.guilds))
