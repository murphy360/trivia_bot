"""Owner-only commands for running the bot."""

import logging

import discord
from discord import app_commands
from discord.ext import commands

log = logging.getLogger(__name__)


async def sync_commands(bot: commands.Bot, interaction: discord.Interaction) -> None:
    """Sync the slash commands with Discord, if the caller owns the bot."""
    if not await bot.is_owner(interaction.user):
        await interaction.response.send_message(
            "Only the bot's owner can sync commands.", ephemeral=True
        )
        return
    await interaction.response.defer(ephemeral=True, thinking=True)
    synced = await bot.tree.sync()
    log.info("commands synced by %s: %d", interaction.user, len(synced))
    await interaction.followup.send(f"Synced {len(synced)} commands.", ephemeral=True)


def admin_group(bot: commands.Bot) -> app_commands.Group:
    """The /admin command group."""
    group = app_commands.Group(name="admin", description="Run the bot (owner only)")

    @group.command(name="sync", description="Sync the slash commands with Discord")
    async def sync(interaction: discord.Interaction) -> None:
        await sync_commands(bot, interaction)

    return group
