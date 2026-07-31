# Session Summary: Mailchimp Newsletter Workflow Codified into the Meetup Skill

**Date**: 2026-07-31
**Duration**: ~2 hours
**Conversation Turns**: ~8 user prompts
**Estimated Cost**: ~$10
**Model**: Fable 5 (claude-fable-5)

## Key Actions

- Debugged the failing `mctx-mcp` Mailchimp MCP server: the endpoint rejected the configured key because it was a Marketing API key, and the Transactional (Mandrill) MCP needs a separate Transactional key.
Mason declined to pay for Transactional, so the MCP is slated for removal.
- Confirmed the Marketing API key works and covers the real need: replicate a campaign, update settings and content, save as draft.
- Created the "PyTexas August 2026 Newsletter" draft by replicating July's campaign and patching title, subject, and preview text.
- First attempt also rewrote the meetup section via `PUT /campaigns/{id}/content`; this silently broke the draft (legacy builder, unfilled template), so it was deleted and recreated settings-only.
- Drafted the August meetup section copy in chat for pasting into the Mailchimp builder, matching the June speaker-month style.
- Added `MAILCHIMP_API_KEY` to `secrets/meetup.sops.env` via `sops set`.
- Codified the entire newsletter workflow into the `meetup-update` skill: new `references/newsletter.md` playbook, Step 4 in SKILL.md, updated frontmatter triggers, and a matching step in the `/update-meetup` command.
- Verified the codified exists-check end to end using `sops exec-env`; found the August draft already scheduled by Mason.
- Added `scripts/scrape_local_meetups.py` and `references/local-meetups.md` to the skill: meetup.com listings render client-side (WebFetch sees zero events), but the `__NEXT_DATA__` Apollo cache in the raw HTML has everything; verified live against all seven network groups.
- Sent updated August announcements to the marketing and organizers Discord channels (manual section removed, Discord/meetup.com event links added, fresh Canva card export attached since signed export URLs expire within hours), then codified the flow as `scripts/send_discord_announcement.py` plus `references/announcements.md`.
- Verified Discord webhooks render markdown masked links (in-channel test), then made the announcements fully deterministic: `scripts/build_announcements.py` renders both channel payloads with masked links from a month-data TOML; templates live in the script, sessions only compose the data file.

## Prompt Inventory

| Prompt/Command | Action Taken | Outcome |
|---|---|---|
| Debug the broken Mailchimp MCP | Read docs, probed endpoint, identified Marketing-vs-Transactional key mismatch | Root cause found; Transactional requires paid add-on |
| What's the command to delete the MCP? | Provided `claude mcp remove mctx-mcp` | Pending user action |
| What can the Mailchimp API do? | Verified key with ping, mapped replicate/patch/content/send endpoints | Confirmed feasible |
| Set up the August draft and update the meetup section | Replicated July, patched settings, PUT new content HTML | Draft created but content PUT silently broke the builder |
| It's a template, you filled in nothing | Deleted broken draft, re-replicated, settings-only, copy drafted for paste | Working draft `bac126a2a4`; API content limit learned |
| Codify into the skill, add key to secrets | Wrote `references/newsletter.md`, updated SKILL.md and command, `sops set` the key | Skill covers the full monthly flow; verified live |
| Commit on a branch | Created `newsletter-workflow-skill` branch, ran session summary flow | This summary |

## Efficiency Insights

**What went well:**
- Probing the MCP endpoint directly with curl found the auth root cause in one call.
- Reading June's sent campaign before drafting August copy made the style match cheap.
- `sops set` added the key without a decrypt/re-encrypt round trip.

**What could improve:**
- Verified the content PUT by GETting it back from the API, which just echoed the write; the Mailchimp UI was the only honest check.
Should have asked Mason to eyeball the draft before declaring success.
- Could have found the "new builder content is API-immutable" limitation in Mailchimp's docs before attempting the PUT.

**Course corrections:**
- Dropped the content-PUT approach entirely after Mason reported the template fallback; the skill now forbids it.

## Process Improvements

- When an API write can only be validated through a UI, say so and hand verification to the user instead of round-tripping through the same API.
- For monthly newsletter work, follow `references/newsletter.md` in the meetup-update skill; it encodes the sharp edges.

## Observations

- June and July 2026 newsletters both went out with the stale subject "PyTexas Monthly April 2026", carried by replication; the skill now mandates setting the subject.
- The newsletter hero image still links to pytexas.org/2024.

## Suggested Skills for Next Session

- `meetup-update`: the next monthly update (September planning or the August archive) should run through the updated skill, including its new newsletter step.
