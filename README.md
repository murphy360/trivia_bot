# trivia_bot

A Discord trivia bot. Servers play the same question at the same moment, and players compete across servers.
Questions come from [trivia_service](https://github.com/murphy360/trivia_service), which writes and fact-checks
them. This bot runs the games and keeps the scores.

It replaces [discord-bot-everything](https://github.com/murphy360/discord-bot-everything). The plan is milestone
[v0.1.0 - Trivia night is back](https://github.com/murphy360/trivia_bot/milestone/1).

## Run it

The bot runs in Docker. Copy `.env.example` to `.env` and fill it in, then:

```bash
docker build -t trivia-bot .
docker run --rm --env-file .env -v "$PWD/data:/data" trivia-bot
```

The log says `ready as <bot name> in <n> servers` when the bot is connected.

The first time, and after any change to the commands, start it once with `SYNC_COMMANDS=true`. You can also run
`/admin sync` in Discord. Only the bot's owner can use it. Discord can take a few minutes to show new commands.

## Settings

| Setting | Required | Default | What it is |
|---|---|---|---|
| `DISCORD_TOKEN` | yes | | The bot token from the Discord developer portal. |
| `TRIVIA_SERVICE_URL` | yes | | Where trivia_service is, for example `http://trivia_service:8000`. |
| `TRIVIA_SERVICE_API_KEY` | yes | | trivia_service's `TRIVIA_SERVICE_API_KEY`. |
| `DATABASE_URL` | no | `sqlite+aiosqlite:////data/trivia_bot.db` | The bot's own store: players, games and scores. |
| `OPS_GUILD_ID` | no | none | The server for ops reports. |
| `OPS_CHANNEL_ID` | no | none | The channel for ops reports. With none set, reports only go to the log. |
| `TIMEZONE` | no | `UTC` | The time zone for Trivia Night, for example `America/New_York`. |
| `SYNC_COMMANDS` | no | `false` | Sync the slash commands with Discord at start-up. |
| `LOG_LEVEL` | no | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`. |

A missing or bad setting stops the bot at start-up with one log line per problem.

## The Discord application

In the [developer portal](https://discord.com/developers/applications), under **Bot**, turn on **Server Members
Intent**. The bot uses it for the player and champion roles. It does not ask for presences or message content.

## Commands

| Command | Who | What it does |
|---|---|---|
| `/admin sync` | the bot's owner | Syncs the slash commands with Discord. |

## Tests

Tests run in Docker:

```bash
docker build -t trivia-bot:test .
docker run --rm -v "$PWD:/src" -w /src trivia-bot:test pytest -q
```
