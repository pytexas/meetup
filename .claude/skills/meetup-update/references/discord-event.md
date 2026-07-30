# Discord Scheduled Event (Pending Token)

The monthly Discord event can be created through Discord's REST API; the pieces exist but the credential is not wired up yet.
Until it is, the Discord event stays a manual step.

## What Already Exists

- Endpoint: `POST https://discord.com/api/v10/guilds/{guild_id}/scheduled-events` with header `Authorization: Bot <token>`.
- Guild ID: `1012382914035597372` (public, from `constants.py` in the pytexas-discord-bot repo).
- The meetup runs in a stage channel, so the event uses `entity_type: 1` (STAGE_INSTANCE) with the stage `channel_id` and `privacy_level: 2`.
  Starting the event auto-creates the stage instance.
- `scheduled_start_time` is the first Tuesday at 8:00 PM Central, sent as ISO 8601 UTC (01:00Z next day during CDT, 02:00Z during CST).

## Payload Template

```json
{
  "name": "PyTexas Virtual Meetup - <Month> <Year>",
  "description": "<Talk Title> - <Speaker Name>\n\n<promo blurb>",
  "scheduled_start_time": "<ISO 8601 UTC>",
  "privacy_level": 2,
  "entity_type": 1,
  "channel_id": "<stage channel id>"
}
```

## What Mason Must Provide

1. A bot token with the Manage Events permission in the guild, stored as `PYTEXAS_DISCORD_BOT_TOKEN` in `secrets/meetup.sops.env`.
   The existing bot's token lives in `infrastructure/secrets/pytexas-discord-bot.sops.env`; whether to reuse it or mint a dedicated one is his call.
2. The stage channel ID, or approval for the skill to fetch it once via `GET /guilds/{guild_id}/channels` and record it here.

Once the token is in secrets, wire the call into Step 10 of the skill and verify with one real event before trusting it monthly.
