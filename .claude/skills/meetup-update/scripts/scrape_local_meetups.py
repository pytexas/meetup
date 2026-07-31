#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.27",
# ]
# ///

"""Scrape upcoming events for the PyTexas network's local meetup groups.

meetup.com renders its event lists client-side, so plain HTML fetches show
zero events. The real data ships inside the page's __NEXT_DATA__ script tag
as an Apollo cache; this script fetches each group page with a browser
user agent and reads events straight out of that JSON.
"""

import argparse
import json
import re

import httpx

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)

# Mirror of https://www.pytexas.org/meetup/local-meetups/
GROUPS: dict[str, str] = {
    "Austin Python User Group": "https://www.meetup.com/austinpython/events/",
    "PyLadies ATX": "https://www.meetup.com/pyladies-atx/events/",
    "Austin Practical Data Science": "https://www.meetup.com/austin-practical-data-science/events/",
    "DFW Pythoneers": "https://www.meetup.com/dfwpython/events/",
    "PyHou": "https://www.meetup.com/python-14/events/",
    "Katy Python Coders": "https://www.meetup.com/katy-python-coders/events/",
    "Alamo Python Learners": "https://www.meetup.com/alamo-python/events/",
}

NEXT_DATA_PATTERN = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
    re.DOTALL,
)


def apollo_state(page_html: str) -> dict[str, dict[str, object]]:
    """Extract the Apollo cache embedded in a meetup.com page.

    Args:
        page_html: Raw HTML of a meetup.com group events page.

    Returns:
        The ``__APOLLO_STATE__`` mapping, or an empty dict when the page
        carries no embedded data (layout change or bot interstitial).
    """
    match = NEXT_DATA_PATTERN.search(page_html)
    if match is None:
        return {}
    next_data = json.loads(match.group(1))
    return next_data.get("props", {}).get("pageProps", {}).get("__APOLLO_STATE__", {})


def group_events(state: dict[str, dict[str, object]], month_prefixes: tuple[str, ...]) -> list[tuple[str, str, str, str]]:
    """Collect matching events from an Apollo cache.

    Args:
        state: Apollo cache from :func:`apollo_state`.
        month_prefixes: ISO month prefixes such as ``("2026-08",)``; empty
            means every listed event.

    Returns:
        Sorted ``(date_time, title, venue, event_url)`` tuples.
    """
    events: set[tuple[str, str, str, str]] = set()
    for cache_key, cache_value in state.items():
        if not cache_key.startswith("Event:") or not isinstance(cache_value, dict):
            continue
        date_time = str(cache_value.get("dateTime", ""))
        if month_prefixes and not date_time.startswith(month_prefixes):
            continue
        venue = ""
        venue_ref = cache_value.get("venue")
        if isinstance(venue_ref, dict) and "__ref" in venue_ref:
            venue_entry = state.get(str(venue_ref["__ref"]), {})
            venue = ", ".join(
                str(part)
                for part in (venue_entry.get("name"), venue_entry.get("city"))
                if part
            )
        events.add(
            (
                date_time,
                str(cache_value.get("title", "?")),
                venue or "online/unlisted",
                str(cache_value.get("eventUrl", "")),
            )
        )
    return sorted(events)


def main() -> None:
    """Entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "months",
        nargs="*",
        help="ISO month prefixes to include, e.g. 2026-08 2026-09; default is all upcoming",
    )
    args = parser.parse_args()
    month_prefixes = tuple(args.months)

    with httpx.Client(
        headers={"User-Agent": USER_AGENT}, follow_redirects=True, timeout=30
    ) as client:
        for group_name, events_url in GROUPS.items():
            print(f"== {group_name}")
            response = client.get(events_url)
            if response.status_code != 200:
                print(f"  fetch failed: HTTP {response.status_code}")
                continue
            state = apollo_state(response.text)
            if not state:
                print("  no embedded event data found (page layout may have changed)")
                continue
            matching_events = group_events(state, month_prefixes)
            for date_time, title, venue, event_url in matching_events:
                cross_post = "  [PyTexas cross-post]" if "PyTexas" in title else ""
                print(f"  {date_time} | {title} | {venue} | {event_url}{cross_post}")
            if not matching_events:
                print("  no matching events listed")


if __name__ == "__main__":
    main()
