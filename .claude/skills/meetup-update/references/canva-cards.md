# Canva Card Decks: Seasons and Naming

The monthly promo cards live in one Canva design per meetup season, one page per month.

## Season Rules

- A season runs September through August, matching the meetup's September 2023 launch (first archived post: `docs/past_meetups/posts/2023-09-11.md`).
- The deck is named "<YYYY> Meetup Banners" where YYYY is the calendar year of the season's ending August.
  A season's deck is created in the August or September that opens it.

## Deck History

- "2024 Meetup Banners": Season 1, September 2023 through August 2024
- "2025 Meetup Banners": Season 2, September 2024 through August 2025
- "2026 Meetup Banners": Season 3, September 2025 through August 2026
- "2027 Meetup Banners": Season 4, September 2026 through August 2027 (starts at the three-year anniversary)

## Picking the Deck for a Meetup

1. Meetup in September through December of year N: deck "<N+1> Meetup Banners".
2. Meetup in January through August of year N: deck "<N> Meetup Banners".
3. If the deck does not exist yet (first card of a new season), ask Mason before creating it; he may want to set the season's look himself.

## Adding a Month's Card

1. Find the deck with the Canva MCP (`search-designs`, query "<YYYY> Meetup Banners").
2. Identify the most recent month's page by reading the page contents (the date text element), not by page position; deck pages are not reliably in chronological order.
3. Copy that page as the base and fill in the talk title, speaker name, meetup date, speaker role line, and headshot.
4. If the editing tools cannot make the change cleanly, stop and give Mason the design's edit URL plus the exact text to place; never leave a half-edited page.

## Mechanics That Are Known to Work

Verified end to end on 2026-07-22 with a test card:

- `copy-design` with `page_numbers` copies a single page into a new design.
- `upload-asset-from-url` imports the headshot, but needs a direct URL that returns HTTP 200; resolve redirects first (e.g. `https://github.com/<user>.png` redirects to `avatars.githubusercontent.com`, which works).
- `replace_text` on the talk title, date, and role elements plus `update_fill` on the editable circular photo element updates the card; commit the transaction to save.

The card layout slots: "Monthly Meetup" heading (fixed), talk title, date ("DD Month YYYY"), time ("8:00 - 9:00pm CST", fixed), "PyTexas Discord Server" (fixed), speaker name, speaker role line, circular headshot, RSVP URL (fixed).
