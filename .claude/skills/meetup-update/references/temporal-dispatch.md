# Temporal Dispatch Workflow

The communication tail of the monthly process runs as the `MonthlyMeetupDispatch` workflow in the pytexas/dispatch repo (renamed from pretix-discord-middleware).
The skill keeps the judgment work; the workflow owns the credentialed API calls.
Status: built 2026-07-30 (pytexas/dispatch#3); not yet deployed (infrastructure#5 carries the rename and the deploy notes).
The dispatch repo's README documents the exact CLI start command and input fields; use it as the source of truth for the handoff, and note the task queue is the service's configured one (default `pretix-discord`).

## Division of Labor

- Skill (laptop, interactive auth): CFP triage, booking over email, website PR, Canva card via the MCP, Drive artifacts.
- Workflow (worker on the droplet): marketing webhook post, organizers webhook post, Discord scheduled event (external, "PyTexas Stage"), meetup.com event once OAuth exists.

## Handoff

After the assets exist, the skill starts the workflow from the CLI:

```bash
temporal workflow start \
  --task-queue meetup-dispatch \
  --type MonthlyMeetupDispatch \
  --input '{"month": "...", "date": "...", "talk": "...", "speaker": "...",
            "canva_link": "...", "card_png_link": "...", "run_of_show_link": "...",
            "attendance_form_link": "...", "rsvp_link": "https://pytexas.org/meetup/join"}'
```

Payload rule: links and strings only, never file bytes.
Temporal caps a payload at 2MB (4MB per gRPC message), and a card PNG can approach that.
The skill uploads the exported card PNG to the month's Drive folder first and passes the link (claim check); the Discord activity downloads and attaches it at post time if an inline image is wanted.

## Workflow Shape

Short-lived dispatch: each API call is one activity with retries, so a failure in one channel retries just that channel instead of double-posting the others.
Reminder timers (T-7 promo nudge, day-after archive nag) are a possible later extension; they were deliberately left out of v1.

## Where the Code Lives

Extend and rename the pretix-discord-middleware repo into a general communications worker (final name Mason's call).
It already has the deploy plumbing in the infrastructure repo: compose project on the droplet, sops env file, ansible deploy.
Renaming means updating those infra references and the sops secret filename.

## Open Items

1. Rename decision and new repo name.
2. Bot token into that service's sops env (Manage Events permission).
3. Meetup.com OAuth credentials (later phase).
4. Build the worker: Python SDK, one workflow, one activity per channel; follow the temporal:temporal-developer skill's Python references when writing it.
