#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pillow>=10"]
# ///

# ABOUTME: Create the monthly PyTexas network event on meetup.com from a month-data TOML.
# Reads MEETUP_API_KEY, MEETUP_API_SECRET, MEETUP_REFRESH_TOKEN from env (run under sops exec-env).

"""Create the monthly PyTexas Virtual Meetup event on meetup.com.

It creates ONE network event on the origin group (pytexas-virtual-meetup-austin)
that propagates to every group in the PyTexas pro network (proNetworkEvents,
propagation left on). The event is ONLINE (venueId "online"), held in Discord;
howToFindUs carries the Discord invite, which is the online event URL.

Auth: Meetup's OAuth refresh token ROTATES on every use, so after each refresh
the new refresh token is written back to secrets/meetup.sops.env. Never run two
of these concurrently.

Events are created as DRAFT by default (visible only to the leadership team).
Publish separately once reviewed (publishEventDraft, or the meetup.com UI).

Required TOML fields: month, year, day, speaker, talk_title, meetup_title,
abstract, topics (list of numeric topic ids). Extra fields are ignored, so the
same month TOML can also feed the Discord and announcement scripts.
Pick topics per references/meetup-event.md (group activeTopics + suggestTopics).

Usage:
    ./create_meetup_event.py september.toml --dry-run
    sops exec-env secrets/meetup.sops.env \\
      './.claude/skills/meetup-update/scripts/create_meetup_event.py september.toml'
"""

import argparse
import datetime as dt
import io
import json
import os
import pathlib
import subprocess
import sys
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

from PIL import Image

TOKEN_URL = "https://secure.meetup.com/oauth2/access"
GQL_URL = "https://api.meetup.com/gql-ext"
GROUP_URLNAME = "pytexas-virtual-meetup-austin"
GROUP_ID = "37176497"  # numeric id of pytexas-virtual-meetup-austin, for photo upload
# Network "all groups" filter (excludedGroupIds: []) for the PyTexas pro network.
# Created via the web UI's createNetworkEventFilter; passing it as proNetworkEvents.filterId
# is what makes the event propagate to every group. Regenerate if it ever stops working.
NETWORK_FILTER_ID = "cd6cdebe-750a-48c5-bad2-f731c4035254"
DISCORD_URL = "https://discord.gg/pytexas"
CENTRAL = ZoneInfo("America/Chicago")
SECRETS = "secrets/meetup.sops.env"
MONTHS = {m: i for i, m in enumerate(
    ["january","february","march","april","may","june","july","august",
     "september","october","november","december"], start=1)}

CREATE_EVENT = """
mutation($input: CreateEventInput!) {
  createEvent(input: $input) {
    event { id title eventUrl status }
    errors { message code field }
  }
}
"""

CREATE_PHOTO = """
mutation($input: GroupEventPhotoCreateInput!) {
  createGroupEventPhoto(input: $input) { uploadUrl photo { id } error { message } }
}
"""


def upload_photo(token: str, event_id: str, image: pathlib.Path) -> str:
    """Register an event photo, PUT the JPEG-converted bytes, return the photo id.

    Meetup's photoscaler only processes JPEG uploads through the API: a raw
    contentType=PNG upload is accepted by S3 (200) but never processed, so the
    image 403s forever. The web UI sidesteps this by converting to JPEG client-side
    (every Meetup CDN photo URL is .jpeg). So convert whatever we're given to JPEG.
    setAsMain makes it the event's featured photo.
    """
    buf = io.BytesIO()
    Image.open(image).convert("RGB").save(buf, "JPEG", quality=90)
    resp = gql(token, CREATE_PHOTO, {"input": {
        "groupId": GROUP_ID, "eventId": event_id, "contentType": "JPEG",
        "photoType": "EVENT_PHOTO", "setAsMain": True,
    }})
    if "errors" in resp:
        sys.exit("photo GraphQL errors: " + json.dumps(resp["errors"], indent=2))
    p = resp["data"]["createGroupEventPhoto"]
    if p.get("error"):
        sys.exit("createGroupEventPhoto error: " + json.dumps(p["error"]))
    put = urllib.request.Request(p["uploadUrl"], data=buf.getvalue(),
                                 method="PUT", headers={"Content-Type": "image/jpeg"})
    code = urllib.request.urlopen(put, timeout=60).status
    if code != 200:
        sys.exit(f"image PUT to S3 returned {code}")
    return p["photo"]["id"]


def refresh_access_token() -> str:
    """Trade the stored refresh token for an access token, persisting the rotated token."""
    data = urllib.parse.urlencode({
        "grant_type": "REFRESH_TOKEN",
        "client_id": os.environ["MEETUP_API_KEY"],
        "client_secret": os.environ["MEETUP_API_SECRET"],
        "refresh_token": os.environ["MEETUP_REFRESH_TOKEN"],
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data, headers={"Accept": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=30).read())
    new = d.get("refresh_token")
    if new and new != os.environ["MEETUP_REFRESH_TOKEN"]:
        subprocess.run(
            ["sops", "set", SECRETS, json.dumps(["MEETUP_REFRESH_TOKEN"]), json.dumps(new)],
            check=True,
        )
    return d["access_token"]


def start_datetime(year: int, month: int, day: int) -> str:
    local = dt.datetime(year, month, day, 20, 0, tzinfo=CENTRAL)
    s = local.strftime("%Y-%m-%dT%H:%M:%S%z")  # offset like -0500
    return s[:-2] + ":" + s[-2:]               # -> -05:00


def build_description(data: dict) -> str:
    return (
        f"Join us for our monthly meetup! The meetup will take place in the "
        f"[PyTexas Discord server]({DISCORD_URL}), so be sure to join!\n"
        f"This month we are excited to be joined by *{data['speaker']}*\n\n"
        f"**Speaker:** *{data['speaker']}*\n"
        f"**Topic:** *{data['talk_title']}*\n\n"
        f"{data['abstract']}"
    )


def build_input(data: dict) -> dict:
    month_num = MONTHS[data["month"].strip().lower()]
    year, day = int(data["year"]), int(data["day"])
    return {
        "groupUrlname": GROUP_URLNAME,
        "title": data["meetup_title"],
        "description": build_description(data),
        "startDateTime": start_datetime(year, month_num, day),
        "duration": "PT1H",
        "venueId": "online",
        "howToFindUs": DISCORD_URL,
        "publishStatus": "DRAFT",
        "topics": [str(t) for t in data["topics"]],
        "proNetworkEvents": {"timezone": "America/Chicago", "filterId": NETWORK_FILTER_ID},
    }


def load(path: pathlib.Path) -> dict:
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    required = ("month", "year", "day", "speaker", "talk_title", "meetup_title", "abstract", "topics")
    missing = [k for k in required if k not in data]
    if missing:
        sys.exit(f"missing required field(s) in {path}: {', '.join(missing)}")
    if not (1 <= len(data["topics"]) <= 5):
        sys.exit(f"topics must have 1-5 ids, got {len(data['topics'])}")
    return data


def gql(token: str, query: str, variables: dict) -> dict:
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(GQL_URL, data=body, headers={
        "Authorization": "Bearer " + token, "Content-Type": "application/json", "Accept": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=60).read())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:1000]}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("toml", type=pathlib.Path)
    parser.add_argument("--image", type=pathlib.Path, help="promo banner to set as the event photo")
    parser.add_argument("--dry-run", action="store_true", help="print the input, send nothing")
    args = parser.parse_args()

    event_input = build_input(load(args.toml))

    if args.dry_run:
        print(json.dumps(event_input, indent=2))
        if args.image:
            print(f"(would upload {args.image} as the event photo)")
        return

    token = refresh_access_token()
    resp = gql(token, CREATE_EVENT, {"input": event_input})
    if "errors" in resp:
        sys.exit("GraphQL errors: " + json.dumps(resp["errors"], indent=2))
    result = resp["data"]["createEvent"]
    if result["errors"]:
        sys.exit("createEvent errors: " + json.dumps(result["errors"], indent=2))
    ev = result["event"]
    print(f"Created {ev['status']} event {ev['id']}")
    print(ev["eventUrl"])

    if args.image:
        photo_id = upload_photo(token, ev["id"], args.image)
        print(f"Uploaded event photo {photo_id}")


if __name__ == "__main__":
    main()
