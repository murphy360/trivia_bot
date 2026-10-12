"""Start the bot: python -m trivia_bot."""

import logging

import discord
from pydantic import ValidationError

from trivia_bot.bot import TriviaBot
from trivia_bot.config import Settings

log = logging.getLogger("trivia_bot")


def load_settings() -> Settings:
    """Read the settings, or exit with one line per problem."""
    try:
        return Settings()
    except ValidationError as error:
        for problem in error.errors():
            name = ".".join(str(part) for part in problem["loc"]).upper()
            log.error("setting %s: %s", name, problem["msg"])
        raise SystemExit(2) from None


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    settings = load_settings()
    logging.getLogger().setLevel(settings.log_level)
    bot = TriviaBot(settings)
    try:
        bot.run(settings.discord_token.get_secret_value(), log_handler=None)
    except discord.LoginFailure:
        log.error("Discord refused the token in DISCORD_TOKEN")
        raise SystemExit(2) from None
    except discord.PrivilegedIntentsRequired:
        log.error(
            "turn on Server Members Intent for the bot in the Discord developer portal"
        )
        raise SystemExit(2) from None


if __name__ == "__main__":
    main()
