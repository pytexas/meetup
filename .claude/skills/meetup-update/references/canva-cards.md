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

Deck pages run newest first: the new month's card always goes in as page 1.
Verify by reading the date text on page 1 before assuming.

The workflow, verified end to end on the real deck on 2026-07-22:

1. Find the deck with the Canva MCP (`search-designs`, query "<YYYY> Meetup Banners").
2. Find the newest single-speaker page (usually page 1, or page 2 when page 1 is the July lightning talks card, which has no headshot slot).
3. Upload the speaker headshot with `upload-asset-from-url`. The URL must return HTTP 200 directly; resolve redirects first (e.g. `https://github.com/<user>.png` redirects to `avatars.githubusercontent.com`, which works).
4. Duplicate that page to the top of the same deck: `merge-designs` with `modify_existing_design`, one `insert_pages` operation sourcing the deck itself and `after_page_number: 0`. Get Mason's go-ahead before this call; it modifies the real deck.
5. `start-editing-transaction` on the deck, then `perform-editing-operations` on page 1 only: `replace_text` for the talk title, date, speaker name, and role line, plus `update_fill` with the uploaded asset on the editable circular photo element.
6. Show Mason the thumbnail, then commit the transaction.
7. If any step cannot complete cleanly, cancel the transaction and give Mason the design's edit URL plus the exact text to place; never leave a half-edited page.

The card layout slots: "Monthly Meetup" heading (fixed), talk title, date ("DD Month YYYY"), time ("8:00 - 9:00pm CST", fixed), "PyTexas Discord Server" (fixed), speaker name, speaker role line, circular headshot, RSVP URL (fixed).

There is no delete-design tool in the MCP; any scratch designs from experiments have to be trashed by Mason in the Canva UI.

Known limitation: the duplicated page inherits the source page's title label (e.g. "June 2026"), and page titles cannot be renamed through the API (confirmed via Canva's help service on 2026-07-22).
After every card, remind Mason to rename the page title in the editor: hover the page thumbnail, ellipsis, pencil icon next to the page title.
