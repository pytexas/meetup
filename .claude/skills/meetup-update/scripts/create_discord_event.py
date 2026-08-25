#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx>=0.27"]
# ///

# ABOUTME: Create the monthly PyTexas Discord scheduled event from a month-data TOML.
# Reads PYTEXAS_DISCORD_BOT_TOKEN from the environment (run under sops exec-env).

"""Create the monthly PyTexas Virtual Meetup Discord scheduled event.

The event is an EXTERNAL event (entity_type 3) located at "PyTexas Stage",
never a stage-linked event: stage-linked events have bad audio quality, so
the meetup avoids them on purpose.

Start and end times are the first Tuesday at 8:00-9:00 PM America/Chicago,
converted to UTC, so DST is handled automatically.

The description reads "Join us this month as <speaker> gives a presentation
about <topic>" followed by a blank line and the abstract. Discord caps the
event description at 1000 characters, so keep the abstract to the concise
summary, not the full CFP text; the script errors if the total is over.

Pass the promo banner with --image to set the event's cover image.

Required TOML fields: month, year, day, speaker, topic, abstract.
(Extra fields are ignored, so the same month TOML can also feed
build_announcements.py.)

Usage:
    # dry run: print the payload (image noted, not embedded), send nothing
    ./create_discord_event.py september.toml --image september-card.png --dry-run

    # real run: needs the bot token in the environment
    sops exec-env secrets/meetup.sops.env \\
      './.claude/skills/meetup-update/scripts/create_discord_event.py september.toml --image september-card.png'
"""

import argparse
import base64
import datetime as dt
import json
import os
import pathlib
import sys
import tomllib
from zoneinfo import ZoneInfo

import httpx

GUILD_ID = "1012382914035597372"  # public, from pytexas-discord-bot constants
CENTRAL = ZoneInfo("America/Chicago")
API = f"https://discord.com/api/v10/guilds/{GUILD_ID}/scheduled-events"
DESCRIPTION_LIMIT = 1000

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}
IMAGE_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif"}


def load(toml_path: pathlib.Path) -> dict:
    with toml_path.open("rb") as fh:
        data = tomllib.load(fh)
    missing = [k for k in ("month", "year", "day", "speaker", "topic", "abstract") if k not in data]
    if missing:
        sys.exit(f"missing required field(s) in {toml_path}: {', '.join(missing)}")
    return data


def utc_iso(year: int, month: int, day: int, hour: int) -> str:
    local = dt.datetime(year, month, day, hour, 0, tzinfo=CENTRAL)
    return local.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def image_data_uri(path: pathlib.Path) -> str:
    mime = IMAGE_MIME.get(path.suffix.lower())
    if not mime:
        sys.exit(f"unsupported image type {path.suffix}; use png, jpg, or gif")
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def build_payload(data: dict, image: pathlib.Path | None) -> dict:
    month_num = MONTHS[data["month"].strip().lower()]
    year, day = int(data["year"]), int(data["day"])
    description = f"Join us this month as {data['speaker']} gives a presentation about {data['topic']}\n\n{data['abstract']}"
    if len(description) > DESCRIPTION_LIMIT:
        sys.exit(
            f"description is {len(description)} chars, over Discord's {DESCRIPTION_LIMIT} limit; "
            "shorten the abstract in the TOML"
        )
    payload = {
        "name": f"PyTexas Virtual Meetup - {data['month']} {year}",
        "description": description,
        "scheduled_start_time": utc_iso(year, month_num, day, 20),
        "scheduled_end_time": utc_iso(year, month_num, day, 21),
        "privacy_level": 2,
        "entity_type": 3,
        "entity_metadata": {"location": "PyTexas Stage"},
    }
    if image is not None:
        payload["image"] = image_data_uri(image)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("toml", type=pathlib.Path, help="month-data TOML file")
    parser.add_argument("--image", type=pathlib.Path, help="promo banner to set as the event cover image")
    parser.add_argument("--dry-run", action="store_true", help="print the payload, send nothing")
    args = parser.parse_args()

    payload = build_payload(load(args.toml), args.image)

    if args.dry_run:
        shown = {**payload}
        if "image" in shown:
            shown["image"] = f"<{args.image} as data URI, {len(payload['image'])} chars>"
        print(json.dumps(shown, indent=2))
        return

    token = os.environ.get("PYTEXAS_DISCORD_BOT_TOKEN")
    if not token:
        sys.exit("PYTEXAS_DISCORD_BOT_TOKEN is not set; run under sops exec-env")

    resp = httpx.post(
        API,
        headers={"Authorization": f"Bot {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    if resp.status_code not in (200, 201):
        sys.exit(f"Discord API returned {resp.status_code}: {resp.text}")

    event = resp.json()
    print(f"Created event {event['id']}")
    print(f"https://discord.com/events/{GUILD_ID}/{event['id']}")


if __name__ == "__main__":
    main()
