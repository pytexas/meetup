# Discord Webhooks

Two webhooks carry the monthly notifications, both stored encrypted in `secrets/meetup.sops.env`:

- `PYTEXAS_MARKETING_WEBHOOK` posts to the marketing channel: the promo asset handoff for social posts.
- `PYTEXAS_MEETUP_WEBHOOK` posts to the meetup organizers channel: the setup summary and outstanding manual steps.

## Configuration

- Set or rotate a URL: `sops secrets/meetup.sops.env` (opens an editor with the decrypted values).
- Onboard another organizer: add their age public key to `.sops.yaml`, then `sops updatekeys secrets/meetup.sops.env`.
- Both webhooks were verified with live test posts on 2026-07-30 (Discord returned 204).

If decryption fails (no sops, no age key), skip the posts and flag them as manual steps.

## Posting

Fire after the Drive artifacts and Canva card exist so every link works.
Show Mason the exact messages in the run summary.

```bash
sops exec-env secrets/meetup.sops.env \
  'curl -sS -X POST "$PYTEXAS_MARKETING_WEBHOOK" -H "Content-Type: application/json" -d "$PAYLOAD"'
```

where `PAYLOAD` is `{"content": "<message>"}`; `sops exec-env` keeps the decrypted URL out of shell history and files.
Same command with `$PYTEXAS_MEETUP_WEBHOOK` for the organizers message.

## Marketing Message Template

Fill only the slots; use "TBD" for links that do not exist yet.

```text
<Month> meetup assets are ready!
* Date: <Weekday>, <Month> <Day> at 8:00 PM Central
* Talk: <Talk Title> - <Speaker Name>
* Promo blurb: <the 2-3 sentence talk abstract from the CFP>
* Card (Canva): <deck link>
* Card image (PNG): <export link>
* Speaker socials for tagging: <handles if provided>
* Run of Show: <Drive doc link>
* Attendance form: <form link>
* Questions form: <form link, or "questions in chat">
* Meetup.com event: TBD (placeholder until API access lands)
* Discord event: TBD (placeholder until the bot token lands; see discord-event.md)
* RSVP: https://pytexas.org/meetup/join
```

Notes on the added lines:

- Card image: run Canva `export-design` for the card's page right before posting; export links are signed URLs, so generate fresh rather than reusing an old one. If the export fails, drop the line and keep the deck link.
- Speaker socials: the CFP form does not collect handles yet; Mason needs to add an optional "Social media handles" question to the form. Until then, omit the line unless the speaker volunteered handles in email.

## Organizers Message Template

```text
<Month> meetup setup is done.
* <Weekday>, <Month> <Day>: <Talk Title> - <Speaker Name>
* Run of Show: <Drive doc link>
* Card (Canva): <deck link>
* Website PR: <PR link>
* Still manual: <remaining items, e.g. Canva page title rename, Discord event, Meetup.com event, headshot>
```

PROPOSED: neither message wording has been used for a real month yet.
Confirm both with Mason on first use, then delete this paragraph.
