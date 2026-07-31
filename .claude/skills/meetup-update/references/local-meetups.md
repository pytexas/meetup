# Local Meetup Lookups (meetup.com)

The run of show doc and the site's local-meetups page both need each network group's next event.
meetup.com renders event lists client-side, so WebFetch (and any HTML-to-markdown fetch) shows "0 upcoming events" for every group regardless of reality.
Do not conclude a group is inactive from a fetch like that.

The real listings ship inside each page's `__NEXT_DATA__` script tag as an Apollo cache, which plain HTTP with a browser user agent can read.
`scripts/scrape_local_meetups.py` does this for every group in the PyTexas network:

```bash
# All upcoming events per group
uv run .claude/skills/meetup-update/scripts/scrape_local_meetups.py

# Only August and September 2026
uv run .claude/skills/meetup-update/scripts/scrape_local_meetups.py 2026-08 2026-09
```

Output is one line per event: date, title, venue, event URL.
Events titled with "PyTexas" are flagged as cross-posts of our own meetup; exclude them when filling in a "their own events" table.

Maintenance notes:

- The group list mirrors <https://www.pytexas.org/meetup/local-meetups/>; keep `GROUPS` in the script in sync when groups join or leave the network.
- "No matching events listed" is trustworthy (the data was present and empty); "no embedded event data found" means meetup.com changed its page structure and the script needs updating.
- Data verified working 2026-07-31.
