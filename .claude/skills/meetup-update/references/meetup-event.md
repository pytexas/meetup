# Meetup.com Network Event

The monthly meetup.com event is created by `scripts/create_meetup_event.py` as a
network event that propagates to all PyTexas groups, with the promo card as its photo.

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
   is not in the group defaults (e.g. "Software Architecture" id 26468).
3. Choose the 5 most relevant ids, always including Python (1064), preferring a
   specific match over generic ones. Put them in the month TOML `topics`.

## Publishing

The script leaves the event as DRAFT. After review, publish with the `publishEventDraft`
mutation (`input: { eventId }`), which flips status to ACTIVE and fans it out. There is
no delete-photo API, so avoid re-uploading a photo more than once per event (each
attempt orphans the previous one as a broken album image); to redo an event cleanly,
delete it (`deleteEvent`) and recreate.
