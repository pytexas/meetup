# Discord Scheduled Event (Pending Token)

The monthly Discord event can be created through Discord's REST API; the pieces exist but the credential is not wired up yet.
Until it is, the Discord event stays a manual step.

## What Already Exists

- Endpoint: `POST https://discord.com/api/v10/guilds/{guild_id}/scheduled-events` with header `Authorization: Bot <token>`.
- Guild ID: `1012382914035597372` (public, from `constants.py` in the pytexas-discord-bot repo).
- The event is created as an EXTERNAL event (`entity_type: 3`) with the location text `PyTexas Stage`, NOT as a stage-linked event.
  Stage-linked events have a bug where the stage audio quality is bad, so the meetup deliberately avoids them; do not "fix" this to entity_type 1.
- External events require `scheduled_end_time` and `entity_metadata.location`, and take no `channel_id`.
- `scheduled_start_time` is the first Tuesday at 8:00 PM Central and `scheduled_end_time` 9:00 PM Central, sent as ISO 8601 UTC (01:00Z/02:00Z next day during CDT, 02:00Z/03:00Z during CST).

## Payload Template

```json
{
  "name": "PyTexas Virtual Meetup - <Month> <Year>",
  "description": "<Talk Title> - <Speaker Name>\n\n<promo blurb>",
  "scheduled_start_time": "<ISO 8601 UTC>",
  "scheduled_end_time": "<ISO 8601 UTC>",
  "privacy_level": 2,
  "entity_type": 3,
  "entity_metadata": {"location": "PyTexas Stage"}
}
```

## What Mason Must Provide

A bot token with the Manage Events permission in the guild, stored as `PYTEXAS_DISCORD_BOT_TOKEN` in `secrets/meetup.sops.env`.
The existing bot's token lives in `infrastructure/secrets/pytexas-discord-bot.sops.env`; whether to reuse it or mint a dedicated one is his call.

Once the token is in secrets, wire the call into Step 10 of the skill and verify with one real event before trusting it monthly.
