#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.27",
# ]
# ///

"""Send a meetup announcement to a PyTexas Discord channel via webhook.

Webhook URLs come from the environment, so run this under sops:

    sops exec-env secrets/meetup.sops.env \\
        './.claude/skills/meetup-update/scripts/send_discord_announcement.py \\
        marketing payload.json --image card.png'

The payload file is a Discord message JSON object, e.g. {"content": "..."}.
An attached image is uploaded into the channel, which outlives the
short-lived signed URLs Canva exports produce.
"""

import argparse
import json
import os
import pathlib
import sys

import httpx

CHANNEL_ENV_VARS: dict[str, str] = {
    "marketing": "PYTEXAS_MARKETING_WEBHOOK",
    "organizers": "PYTEXAS_MEETUP_WEBHOOK",
}


def main() -> None:
    """Entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("channel", choices=sorted(CHANNEL_ENV_VARS))
    parser.add_argument("payload", type=pathlib.Path, help="Discord message JSON file")
    parser.add_argument(
        "--image", type=pathlib.Path, help="Optional image to attach (PNG/JPG)"
    )
    args = parser.parse_args()

    env_var = CHANNEL_ENV_VARS[args.channel]
    webhook_url = os.environ.get(env_var)
    if not webhook_url:
        sys.exit(
            f"{env_var} is not set; run under "
            "'sops exec-env secrets/meetup.sops.env ...'"
        )

    payload_text = args.payload.read_text()
    json.loads(payload_text)  # fail fast on malformed payload

    files: dict[str, tuple[str, bytes, str]] = {
        "payload_json": ("", payload_text.encode(), "application/json"),
    }
    if args.image is not None:
        suffix = args.image.suffix.lstrip(".").lower() or "png"
        files["files[0]"] = (args.image.name, args.image.read_bytes(), f"image/{suffix}")

    response = httpx.post(f"{webhook_url}?wait=true", files=files, timeout=30)
    response.raise_for_status()
    message = response.json()
    attachment_names = [attachment["filename"] for attachment in message.get("attachments", [])]
    print(f"sent to {args.channel}: message id {message['id']}, attachments {attachment_names}")


if __name__ == "__main__":
    main()
