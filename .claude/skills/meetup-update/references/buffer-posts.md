# Social Posts via Buffer

The monthly meetup gets two rounds of social posts from the PyTexas Buffer account (organization "My Organization", account conference@pytexas.org, timezone America/Chicago), one round about a week out and one the morning of the meetup.
This file records the pattern read out of the August through November 2026 posts and how the skill reproduces it.
Buffer is a connected claude.ai MCP; call `get_account` first and `list_channels` for IDs rather than hardcoding them (this repo is public).

## Channels

All five channels get every meetup post: Facebook page "PyTexas Foundation", X "pytexas", Bluesky "pytexas.org", Mastodon "pytexas" (fosstodon.org), LinkedIn page "pytexas-foundation".

## The Two Rounds

| Round | When | Mode | Observed dates |
| --- | --- | --- | --- |
| Announcement | 3 to 7 days before the meetup | `addToQueue` (next free slot on each channel) | Aug 1 for Aug 4, Aug 26 for Sep 1, Sep 29 for Oct 6, Oct 30 for Nov 3 |
| Day-of | the meetup morning, roughly 8:00 to noon Central | `customScheduled` | Aug 4, Sep 1, Oct 6, Nov 3 |

Queue slots (Central) at the time of writing: X 10:19 and 12:15, Bluesky 10:30, Mastodon 11:30, LinkedIn 11:51, Facebook varies by weekday.
`addToQueue` fires at the next free slot, which is fine when the posts are made a few days out but wrong when the skill runs two or three weeks ahead. So the skill uses `customScheduled` for both rounds: the announcement round on the Tuesday one week before the meetup, the day-of round on the meetup date, each at 9:00 (Facebook), 9:19 (X), 10:30 (Bluesky), 11:30 (Mastodon), 11:51 (LinkedIn) Central. December 2026 was scheduled this way.

Every post:

- has the month's promo card as its single image asset (1600x900 PNG from the Canva deck). Buffer does **not** re-host an API-supplied image at create time; it keeps the URL and fetches it at publish, so a signed Canva export link (hours of life) would be dead by the due date. Commit the card to the repo as `docs/assets/images/cards/YYYY-MM.png` and use the commit-pinned raw URL `https://raw.githubusercontent.com/pytexas/meetup/<commit sha>/docs/assets/images/cards/YYYY-MM.png`, which survives branch deletion and squash merges. Verified 2026-11-11.
- carries the tag "Monthly Meetup" (Buffer tag id from `list_posts` output; August also carried "Training" for a talk that was a workshop)
- uses `schedulingType: automatic`

## Copy Template

Three parts, separated by blank lines:

1. **Hook.** One or two sentences from the abstract, trimmed, with `#PyTexas` and `#Python` worked in and one topic hashtag (`#ThreatModeling`, `#SoftwareEngineering`). The speaker's name appears when it reads naturally ("Nishanth Sirikonda reframes architecture as..."). Name only, never the employer (SKILL.md Content Guidelines).
2. **Call to action.** Announcement: `Join us <Mon D> @ 8p CST in our Discord to learn more!` Day-of: `Join us TONIGHT @ 8p CST in our Discord to learn more!`
3. **Link.** `http://pytexas.org/meetup` on its own line.

Two lengths:

- **Long** (Facebook, LinkedIn, Mastodon): the full hook.
- **Short** (X, Bluesky): the same hook cut to fit X's 280 characters including the link; Bluesky allows 300 but gets the X text so the two stay identical.

November 2026 long version, for reference:

```text
Security problems rarely begin as such. This #PyTexas talk introduces #ThreatModeling as a lightweight habit for #Python teams building AI, data, and cloud-connected systems, focused on collaboration patterns that help developers, security teams, and product stakeholders reason together.

Join us Nov 3 @ 8p CST in our Discord to learn more!
http://pytexas.org/meetup
```

## Procedure

1. `get_account` for the organization id and `currentTime`; `list_channels` for the five channel ids.
2. Write the long and short copy from the month TOML's `abstract` and `talk_title`; check the short version is 280 characters or fewer.
3. Commit the card PNG to `docs/assets/images/cards/YYYY-MM.png` on the month's branch, push, and use the commit-pinned raw URL as the image asset, with alt text "<Month> <Year> PyTexas Meetup promo card: <talk title> with <speaker>, <date> at 8pm Central in the PyTexas Discord".
4. Show Mason all ten posts (two rounds, five channels) with their mode and times.
5. **Only on Mason's explicit yes:** create them, applying the 72-hour rule he set on 2026-11-11: a post whose due time is more than 72 hours away goes straight to `scheduled` (someone will see it in Buffer before it fires); a post due within 72 hours is created with `saveToDraft: true` for him to approve in the UI. Both rounds use `customScheduled` with `dueAt`. Never `shareNow`.
6. Report the ten post ids. Edits go through `edit_post`; a wrong post is removed with `delete_post` before its due time.

Facebook posts need `metadata.facebook.type: "post"`.
`delete_post` removes a post from Buffer only; anything already published stays on the network, so the same consent rule as the Discord webhooks applies (SKILL.md Step 10).
