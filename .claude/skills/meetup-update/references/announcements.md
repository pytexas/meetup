# Discord Announcements (Marketing and Organizers Channels)

After the monthly setup is complete, two Discord channels get an announcement via webhooks stored in `secrets/meetup.sops.env`:

- `PYTEXAS_MARKETING_WEBHOOK`: the marketing channel; audience prepares social posts
- `PYTEXAS_MEETUP_WEBHOOK`: the meetup organizers channel; audience runs the meetup

The flow is two scripts; never hand-write the message text or the curl:

```bash
# 1. Fill in a month-data TOML (field list in the script's docstring), then render both payloads
uv run .claude/skills/meetup-update/scripts/build_announcements.py august.toml

# 2. Send each payload with the card attached
sops exec-env secrets/meetup.sops.env \
  './.claude/skills/meetup-update/scripts/send_discord_announcement.py marketing marketing.json --image card.png'
sops exec-env secrets/meetup.sops.env \
  './.claude/skills/meetup-update/scripts/send_discord_announcement.py organizers organizers.json --image card.png'
```

The message templates live in `build_announcements.py` and are the single source of truth; the data file is the only thing a session composes.
Long URLs are rendered as markdown masked links (`[Run of Show](url)`), which Discord renders for webhook messages (verified in-channel 2026-07-31).

## Card Image Handling

The promo card lives in the "2026 Meetup Banners" Canva deck (design id `DAGv-Ktk4IM`, share link <https://www.canva.com/d/aiHt9RXm1DY_dI7>), one page per month.
Canva export URLs are signed and expire within hours, so always attach the PNG to the message (`--image`) in addition to quoting the download link; the attachment persists in Discord after the link dies.
Always state the link's expiry time next to it and note that re-export happens from the deck.

## Message Content

Both messages are rendered by `build_announcements.py`; edit the templates there, not here.
Marketing gets the full asset rundown (date, talk, blurb, card, run of show, forms, event links, RSVP); organizers gets the logistics-only subset plus the website PR status.
Populate `still_manual` in the data file with any incomplete steps and the organizers message ends with a `Still manual:` line; leave it empty (or omit it) once everything is done.

## Gotchas Learned the Hard Way

- The attendance form link must be the published responder link (forms.gle or `/d/e/...`), never the `/d/<id>/viewform` edit-ID URL, which only works for the owner. Verify it with an unauthenticated fetch before sending.
- The canonical meetup.com event lives on the PyTexas Virtual Meetup group (<https://www.meetup.com/pytexas-virtual-meetup-austin/>); the copies on other network groups' pages are cross-posts. Use `scripts/scrape_local_meetups.py` techniques (or that group's events page) to find it.
- Webhook success with `?wait=true` returns HTTP 200 and the created message JSON; check the message id and attachment list rather than assuming delivery.
- Sent messages cannot be deleted through the webhook (attempts 404). Treat every send as permanent: get the payload right first, and fix mistakes with a follow-up message or ask Mason to clean up in-channel.
