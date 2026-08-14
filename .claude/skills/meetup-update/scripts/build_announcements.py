#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///

"""Render the monthly Discord announcement payloads from a month-data TOML file.

The templates in this file are the single source of truth for both channel
messages; sessions fill in a data file, never the message text. Produces
marketing.json and organizers.json next to the data file, ready for
send_discord_announcement.py.

Example data file:

    month = "August"
    year = 2026
    weekday = "Tuesday"
    day = 4
    talk_title = "Cutting Through the Slop: Lessons Learned from a Year of Claude Code"
    speaker = "Mason Egger"
    blurb = "Code is cheaper than it's ever been..."
    deck_page = 1
    card_download_url = "https://export-download.canva.com/..."
    card_expiry = "4:38 PM Central today"
    run_of_show_url = "https://docs.google.com/document/d/.../edit"
    attendance_url = "https://forms.gle/..."
    meetup_event_url = "https://www.meetup.com/pytexas-virtual-meetup-austin/events/.../"
    discord_event_url = "https://discord.com/events/.../..."
    website_pr_url = "https://github.com/pytexas/meetup/pull/47"
    website_pr_status = "merged"
    still_manual = []  # optional; organizers message gets a Still manual line if non-empty
"""

import argparse
import json
import pathlib
import sys
import tomllib

DECK_URL = "https://www.canva.com/d/aiHt9RXm1DY_dI7"
DECK_NAME = "2026 Meetup Banners"
RSVP_URL = "https://pytexas.org/meetup/join"
DISCORD_CONTENT_LIMIT = 2000

REQUIRED_FIELDS = (
    "month",
    "year",
    "weekday",
    "day",
    "talk_title",
    "speaker",
    "blurb",
    "deck_page",
    "card_download_url",
    "card_expiry",
    "run_of_show_url",
    "attendance_url",
    "meetup_event_url",
    "discord_event_url",
    "website_pr_url",
    "website_pr_status",
)

MARKETING_TEMPLATE = """\
{month} {year} meetup: everything is live!
* Date: {weekday}, {month} {day} at 8:00 PM Central
* Talk: {talk_title} - {speaker}
* Promo blurb: {blurb}
* Card: [{deck_name}, page {deck_page}]({deck_url}); image attached below, or [download the PNG]({card_download_url}) (link expires {card_expiry}; re-export from the deck after that)
* [Run of Show]({run_of_show_url})
* [Attendance form]({attendance_url})
* Questions: in chat tonight
* [Meetup.com event]({meetup_event_url}) (cross-posted to all network groups)
* [Discord event]({discord_event_url})
* [RSVP]({rsvp_url})"""

ORGANIZERS_TEMPLATE = """\
{month} {year} meetup setup is done.
* {weekday}, {month} {day} at 8:00 PM Central: {talk_title} - {speaker}
* [Run of Show]({run_of_show_url})
* Card: [{deck_name}, page {deck_page}]({deck_url}); image attached, or [download the PNG]({card_download_url}) (link expires {card_expiry})
* [Discord event]({discord_event_url})
* [Meetup.com event]({meetup_event_url})
* [Attendance form]({attendance_url})
* [Website PR]({website_pr_url}) ({website_pr_status})"""


def main() -> None:
    """Entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_file", type=pathlib.Path, help="Month data TOML file")
    args = parser.parse_args()

    data = tomllib.loads(args.data_file.read_text())
    missing_fields = [field for field in REQUIRED_FIELDS if field not in data]
    if missing_fields:
        sys.exit(f"missing fields in {args.data_file}: {', '.join(missing_fields)}")

    context = dict(data, deck_url=DECK_URL, deck_name=DECK_NAME, rsvp_url=RSVP_URL)

    organizers_text = ORGANIZERS_TEMPLATE.format(**context)
    still_manual = data.get("still_manual", [])
    if not isinstance(still_manual, list):
        sys.exit(f"still_manual must be a list of strings, got {type(still_manual).__name__}")
    if still_manual:
        organizers_text += "\n* Still manual: " + "; ".join(still_manual)

    messages = {
        "marketing": MARKETING_TEMPLATE.format(**context),
        "organizers": organizers_text,
    }
    # Check every message before writing any, so an oversize one never leaves a
    # partial set of payloads on disk for a later send step to pick up.
    for channel, content in messages.items():
        if len(content) > DISCORD_CONTENT_LIMIT:
            sys.exit(f"{channel} message is {len(content)} chars, over Discord's {DISCORD_CONTENT_LIMIT}")
    for channel, content in messages.items():
        output_path = args.data_file.parent / f"{channel}.json"
        output_path.write_text(json.dumps({"content": content}) + "\n")
        print(f"wrote {output_path} ({len(content)} chars)")


if __name__ == "__main__":
    main()
