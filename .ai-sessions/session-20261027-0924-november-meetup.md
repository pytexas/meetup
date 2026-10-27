# Session Summary: November 2026 Meetup Setup

**Date**: 2026-10-27
**Duration**: ~40 minutes
**Conversation Turns**: 4 (`/meetup-update`, then "Canva is updated. Try again.")
**Estimated Cost**: moderate (MCP-heavy status checks, Drive and Mailchimp writes, site edits)
**Model**: Claude Fable 5.1

## Key Actions

- Confirmed Chakra Pavan Kumar Kota is booked for Nov 3 from the Gmail "Speak at PyTexas Meetup" thread (Mason booked him 7/31; Pavan confirmed 8/1). He was already on the homepage with headshot and author entry.
- Archived the October 6 meetup (Shayan Ali) to `docs/past_meetups/posts/2026-10-06.md` and removed the October section from `docs/index.md`; `mkdocs build` passes.
- Created the November Mailchimp draft (`31eb052dbc`) by replicating the October issue and PATCHing title, subject, and preview text.
- Created the Drive month folder `2026-11-03`, copied both forms from the template folder, and uploaded the run of show as markdown (converted cleanly; FILL_ME_IN markers and the table survived).
- Wrote the month TOML in the scratchpad and dry-ran both event scripts; picked meetup.com topics via `suggestTopics` (Cybersecurity 152026, Application Security 50280, Software Security 447162, plus Python and AI).
- Canva: the connector is on Mason's personal account (search shows personal designs; the banners deck returns "Not allowed to access design"). Card flagged as manual with the deck link and exact text.
- After Mason reconnected the Canva connector: uploaded the headshot, duplicated the October page to the top of the 2027 deck, filled title/date/name/role/headshot, widened the name box so the long name stays on one line, committed, and exported the PNG.
- Created the Discord scheduled event (1564647667966152817) and the meetup.com DRAFT network event (317161034) with the card attached; both announcement payloads rendered but held until the forms are published.
- Drafted (not sent) the date-offer email to Kriti Faujdar for Dec 1 / Jan 5 / Feb 2. Sridhar Irujolla was offered dates on 7/22 and never replied; left for Mason to decide.

## Prompt Inventory

| Prompt/Command | Action Taken | Outcome |
|---|---|---|
| `/meetup-update` | Status audit (Todoist, CFP sheet, Gmail, site, Mailchimp, Drive, Canva, Discord, meetup.com), then website archive, newsletter draft, Drive artifacts, TOML, dry runs, outreach draft | Website on branch `november-meetup`; artifacts created except the Canva card and the items that depend on it |

## Efficiency Insights

**What went well:**
- The status audit found November already on the live site, so the CFP-to-homepage steps collapsed to a single archive post.
- Importing `refresh_access_token` and `gql` from `create_meetup_event.py` gave a safe way to run `suggestTopics` without duplicating the token-rotation logic.

**What could improve:**
- `suggestTopics` returns a `TopicsConnection`; the first query used the wrong shape and cost a token rotation.

**Course corrections:**
- Canva search by deck name returned nothing before the account mismatch was obvious; a `modified_descending` listing diagnosed it in one call.

## Process Improvements

- Add a Canva account check to `canva-cards.md` mirroring the Drive one: list recent designs first, and if they are not PyTexas designs, stop and ask Mason to reconnect.
- Record the `suggestTopics` query shape (`edges { node { id name } }`) in `meetup-event.md`.

## Observations

- The Sept 6 outreach drafts for Kriti and Sridhar no longer exist and were never sent (no messages to Kriti anywhere in the mailbox).
- Each `refresh_access_token` call rotates `MEETUP_REFRESH_TOKEN`; the rotated value is on this branch.

## Suggested Skills for Next Session

- `meetup-update`: once the Canva connector is on the PyTexas account, finish the November card, then run the Discord and meetup.com scripts with `--image` and send both announcements.
