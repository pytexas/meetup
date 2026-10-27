# Session Summary: Meetup.com Event Goes Manual by Default

**Date**: 2026-10-27
**Duration**: ~20 minutes (same conversation as the November setup)
**Conversation Turns**: 3 (dashboard screenshot showing "Cancelled"; "publish the draft"; "give me the info and I'll create it myself")
**Estimated Cost**: moderate (several read-only GraphQL inspections, one publish)
**Model**: Claude Fable 5.1

## Key Actions

- Diagnosed the "Cancelled" row: event 317161034 was DRAFT with its network record CANCELLED on creation; October's dashboard-created event had a healthy PAST record.
- With Mason's go-ahead ran `publishEventDraft`: event went ACTIVE on the origin group, network record stayed CANCELLED through 20s of polling, no cross-posts on any of the other groups, and the network's own event search did not count it.
- Found the script's JPEG photo upload (536830936) was never processed by the photoscaler (403); Mason's UI upload (536831239) serves fine. A dashboard edit-and-publish by Mason did not revive the network record either.
- Per Mason, made manual creation the default: SKILL.md Overview, Step 11, and the handoff banner now hand him a paste block; `meetup-event.md` leads with the paste block and keeps the script as opt-in with the 2026-10-27 findings; `announcements.md` says the URL comes from Mason.

## Prompt Inventory

| Prompt/Command | Action Taken | Outcome |
|---|---|---|
| Screenshot: event created then "Cancelled" | Read-only GraphQL inspection of both months' events and the schema | Network record cancelled, event fine |
| "Go ahead and publish the draft" | `publishEventDraft`, polled, scanned groups, searched the network | Live on Austin only, no fan-out |
| "Set the default to just give me the info" | Skill and reference edits | Manual default committed |

## Efficiency Insights

**What went well:**
- Importing the script's auth helpers kept every inspection to one small file and persisted each rotated token.

**What could improve:**
- Mason's verdict: more time debugging the API than it took to create the event by hand. The reference already warned that publish cancels propagation; a working-but-partial automation should have been demoted sooner.

**Course corrections:**
- Stopped proposing further API fixes once Mason said to default to manual.

## Process Improvements

- When an automation needs a human finishing step that the human then has to debug, make the human step the default and keep the automation opt-in.

## Observations

- `NetworkEvent` exposes `status`, `isAnnounced`, `groupCount`; `proNetwork.eventsSearch` takes `eventDateMin`/`eventDateMax`, not a status enum.
- This branch was cut before PR #58 merged, so SKILL.md still carries the old Fallback A text here; expect a small merge conflict in SKILL.md between #58 and #59.

## Suggested Skills for Next Session

- `meetup-update`: December run uses the paste block for meetup.com.
