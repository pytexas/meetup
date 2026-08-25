# Discord Scheduled Event

The monthly Discord event is created through Discord's REST API by `scripts/create_discord_event.py`.
The bot token is wired up, so this step is automated.

## Running It

```bash
# dry run: print the payload, send nothing (no token needed)
uv run .claude/skills/meetup-update/scripts/create_discord_event.py september.toml \
  --image september-card.png --dry-run

# real run
sops exec-env secrets/meetup.sops.env \
  './.claude/skills/meetup-update/scripts/create_discord_event.py september.toml --image september-card.png'
```

On success it prints the event id and URL (`https://discord.com/events/<guild>/<event_id>`).
Always dry-run first to eyeball the description and times.

## Input

The script reads a month-data TOML. Required fields: `month`, `year`, `day`, `speaker`, `topic`, `abstract`.
Extra fields are ignored, so the same TOML can also feed `build_announcements.py`.

- `topic` is a short phrase; the description reads "Join us this month as \<speaker\> gives a presentation about \<topic\>".
- `abstract` follows after a blank line. Keep it to the concise summary: Discord caps the event description at 1000 characters and the script errors if the intro plus abstract runs over.
- `--image` sets the event cover image (the month's promo card PNG). Attach it every month; it is embedded as a base64 data URI in the create call.

Discord center-crops the cover to its own strip and the API has no crop/position/anchor field, so you cannot nudge it from code. The card template in the Canva deck is laid out to survive that center crop, so pass the card PNG as-is. Do not letterbox or pad it; that was tried and looked worse.

## How the Event Is Built

- Endpoint: `POST https://discord.com/api/v10/guilds/{guild_id}/scheduled-events` with header `Authorization: Bot <token>`.
- Guild ID `1012382914035597372` (public, from `constants.py` in the pytexas-discord-bot repo) is hardcoded in the script.
- EXTERNAL event (`entity_type: 3`) with location text `PyTexas Stage`, NOT a stage-linked event. Stage-linked events have bad stage audio, so the meetup avoids them on purpose; do not "fix" this to `entity_type: 1`.
- External events require `scheduled_end_time` and `entity_metadata.location` and take no `channel_id`.
- Times are the first Tuesday 8:00-9:00 PM `America/Chicago`, converted to UTC via `zoneinfo`, so CDT/CST is handled without a hardcoded offset.

## Credential

`PYTEXAS_DISCORD_BOT_TOKEN` in `secrets/meetup.sops.env`, reused from the existing pytexas-discord-bot (`DISCORD_TOKEN` in `infrastructure/secrets/pytexas-discord-bot.sops.env`).
The bot's role needs the **Manage Events** permission in the guild, or the POST returns `403 Missing Permissions` (code 50013). That permission is granted.

## Fixing an Event After Creation

The script only creates. To change a live event, delete it and recreate:

```bash
sops exec-env secrets/meetup.sops.env \
  'curl -s -o /dev/null -w "%{http_code}\n" -X DELETE \
   -H "Authorization: Bot $PYTEXAS_DISCORD_BOT_TOKEN" \
   "https://discord.com/api/v10/guilds/1012382914035597372/scheduled-events/<event_id>"'
```

A successful delete returns 204. Recreate with the corrected TOML or image.
