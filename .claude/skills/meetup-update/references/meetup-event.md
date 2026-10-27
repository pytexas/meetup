# Meetup.com Network Event

**Default: Mason creates the event in the pro dashboard from a paste block the skill
renders.** Set on 2026-10-27 after the API path cost more debugging than it saved: a
network event created through `createEvent` with `proNetworkEvents` now arrives with
its network record CANCELLED, `publishEventDraft` makes the event ACTIVE on the origin
group but does not revive the record (no fan-out to the other nine groups), editing and
publishing from the dashboard did not revive it either, and the script's JPEG photo
upload was accepted but never processed by the photoscaler (403 forever), so the card
did not show. The script below still exists for the parts that worked (title, body,
time, topics) and for whenever Meetup fixes this; use it only when Mason asks.

## Default: The Paste Block

Render the event fields with the script's dry run, which performs no API calls and
needs no token:

```bash
uv run .claude/skills/meetup-update/scripts/create_meetup_event.py november.toml --dry-run
```

Then put this block in the handoff banner (SKILL.md Step 7), filled from the dry-run
output and the month TOML. Topic names come from the ids in `topics` (see Topics
below for the common ones).

```text
meetup.com network event (create in the pro dashboard, group: PyTexas Virtual Meetup)
Title:       <meetup_title>
Date/time:   <Weekday>, <Month> <Day>, <Year>, 8:00 PM - 9:00 PM Central
Location:    Online; event link https://discord.gg/pytexas
Topics:      <topic names, up to 5, Python first>
Photo:       <absolute path to the month's card PNG; also attached in the Discord payload>
Network:     use the all-groups network filter so it fans out to every PyTexas group

Description (paste as-is):
<the "description" field from the dry run, verbatim>
```

When the URL comes back, put it in `meetup_event_url` in the month TOML; both Discord
announcements link it.

The MKE Python Meetup group (<https://www.meetup.com/mke-python-meetup/>) is not in the
pro network, so the fan-out never reaches it; Mason creates a second copy there from the
same block. Check it with a plain fetch of the group's events page and the `__NEXT_DATA__`
parse from `local-meetups.md`; the Austin origin stays the canonical link.

## What the fan-out actually does (2026-10-27)

The API fan-out does create the per-group copies at creation time (their ids run
consecutively after the origin's), but they stay hidden while the network record reads
CANCELLED. Duplicating the event in the pro dashboard and publishing the duplicate is
what flipped the original set live and marked it announced; the duplicate itself came
out dated the next day and had to be deleted by hand. Also: the dashboard's duplicate
defaults the date to tomorrow, so check the date before publishing.

## Script Path (Opt-In Only)

Everything below describes `scripts/create_meetup_event.py`, kept for the day the API
behaves. As of 2026-10-27 it creates a usable single-group event and nothing more.

## Running It

```bash
# dry run: print the createEvent input, send nothing
uv run .claude/skills/meetup-update/scripts/create_meetup_event.py september.toml \
  --image september-card.png --dry-run

# real run: creates the event as a DRAFT
sops exec-env secrets/meetup.sops.env \
  './.claude/skills/meetup-update/scripts/create_meetup_event.py september.toml --image september-card.png'
```

It prints the event id and URL, and (with `--image`) the uploaded photo id.
Events are created as DRAFT. Publish after review (see Publishing).

## Input

Same month-data TOML as the other scripts. Required for this one: `month`, `year`,
`day`, `speaker`, `talk_title` (full, for the Topic line), `meetup_title` (the short
event title, since long titles get truncated on the card), `abstract`, `topics`
(1-5 numeric topic ids). See Topics below.

The event body is built to match past network events: a "Join us for our monthly
meetup..." intro linking the Discord server, then **Speaker:** / **Topic:** lines,
then the abstract. Time is the first Tuesday 8:00-9:00 PM `America/Chicago`
(`PT1H`), `venueId: "online"`, and `howToFindUs` holds the Discord invite (that
field is the online event's URL).

## Auth

Meetup's API uses OAuth. The consumer key/secret alone cannot mint a token headless:
the only grant types the token endpoint accepts are `AUTHORIZATION_CODE` (one-time
browser authorize) and `REFRESH_TOKEN`. So there was a one-time browser authorize to
get a refresh token; from then on the script trades the refresh token for an access
token silently.

Secrets in `secrets/meetup.sops.env`:

- `MEETUP_API_KEY`, `MEETUP_API_SECRET` — the OAuth consumer key/secret.
- `MEETUP_REFRESH_TOKEN` — the long-lived token.

**The refresh token ROTATES on every use.** Meetup returns a new refresh token each
refresh and invalidates the old one, so the script writes the new one back to sops on
every run. Never run two calls concurrently, and if a run dies mid-refresh the token
in sops is still the last good one.

To re-authorize from scratch (if the refresh token is ever lost/revoked): open
`https://secure.meetup.com/oauth2/authorize?client_id=<KEY>&response_type=code&redirect_uri=https://pytexas.org&scope=event_management`,
click allow, copy the `code` from the `https://pytexas.org/?code=...` redirect, and
POST it (`grant_type=AUTHORIZATION_CODE`, client id/secret, redirect_uri, code) to
`https://secure.meetup.com/oauth2/access`; store the returned refresh token.

## Network Event (propagation to all groups)

The endpoint is `https://api.meetup.com/gql-ext`. The account (`PyTexas Foundation`)
is the pro-network primary organizer of 10 groups. The event is created on the origin
group `pytexas-virtual-meetup-austin` and propagates via `proNetworkEvents`:

```
proNetworkEvents: { timezone: "America/Chicago", filterId: "<network filter id>" }
```

The `filterId` is a **network event filter** (an "all groups" filter =
`excludedGroupIds: []`). It's created in the web UI's `createNetworkEventFilter` and
is baked into the script as `NETWORK_FILTER_ID`. Without it the event does not
propagate. `networkEvent` on the created event reads `null` for a few seconds after
creation, then populates; that lag is normal, not a failure.

## The Photo (must be JPEG)

Photos are a two-step upload: `createGroupEventPhoto` returns a presigned S3
`uploadUrl` + photo id, then PUT the bytes to that URL. `setAsMain: true` makes it the
event's featured photo.

**Convert the image to JPEG first.** Meetup's photoscaler only processes JPEG uploads
through the API; a `contentType: PNG` upload is accepted by S3 (200) but never
processed, so it 403s forever. The web UI hides this by converting to JPEG
client-side (every Meetup CDN photo URL is `.jpeg`). The script converts whatever it
is given to JPEG. Processing takes a few seconds; the CDN URL 403s until then.

## Topics (event tags, up to 5)

Meetup allows 5 topic tags; fill all 5 when you can. Pick per talk:

1. Read the group's `activeTopics` (`groupByUrlname(urlname:"...").activeTopics`).
2. Run `suggestTopics(query:"<talk keyword>")` to find a specific catalog topic that
   is not in the group defaults (e.g. "Software Architecture" id 26468). It returns a
   connection, so select `suggestTopics(query:$q){ edges { node { id name } } }`.
   Reuse `refresh_access_token()` and `gql()` from the script (import it by file
   path) so the rotated refresh token is still written back to sops; every call
   rotates it. Security talks: Cybersecurity 152026, Application Security 50280,
   Software Security 447162.
3. Choose the 5 most relevant ids, always including Python (1064), preferring a
   specific match over generic ones. Put them in the month TOML `topics`.

## Publishing

The script leaves the event as DRAFT. `publishEventDraft` (`input: { eventId }`) flips
the event to ACTIVE on the origin group only; on 2026-10-27 the network record stayed
CANCELLED through the publish and through a dashboard edit-and-publish, so there was
no fan-out. There is no delete-photo API, so avoid re-uploading a photo more than once
per event (each attempt orphans the previous one as a broken album image); to redo an
event cleanly, delete it (`deleteEvent`) and recreate.

## Reading Event State

Read-only check of an event and its network record, reusing the script's auth helpers
(each call rotates the refresh token, which the helper persists):

```graphql
{ event(id:"<id>"){ id status networkEvent { id status isAnnounced groupCount }
  featuredEventPhoto { id highResUrl } } }
```

A healthy network event shows `networkEvent.status` ACTIVE (PAST after the date) and
the photo's `highResUrl` returns 200. `proNetwork(urlname:"pytexas").eventsSearch`
with an `eventDateMin`/`eventDateMax` filter lists what the network itself counts.
