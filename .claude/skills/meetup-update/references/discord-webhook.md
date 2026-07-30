# Marketing Channel Webhook

The monthly promo notification goes to the marketing channel in the PyTexas Discord via a webhook.
There is no emailed social media asset handoff; this post is the handoff.

## Configuration

The webhook URL lives encrypted in `secrets/meetup.sops.env` (key `PYTEXAS_MARKETING_WEBHOOK`), following the same sops + age pattern as the pytexas/infrastructure repo.
The encrypted file is safe to commit publicly; only the age recipients listed in `.sops.yaml` can decrypt it.

- Set or rotate the URL: `sops secrets/meetup.sops.env` (opens an editor with the decrypted values).
- Onboard another organizer: add their age public key to `.sops.yaml`, then `sops updatekeys secrets/meetup.sops.env`.
- The real webhook URL is stored and was verified with a live test post on 2026-07-30 (Discord returned 204).

If decryption fails (no sops, no age key), skip the post and flag it as a manual step.

## Posting

Fire only after the Canva card exists so the link works.
Show Mason the exact message in the run summary.

```bash
sops exec-env secrets/meetup.sops.env \
  'curl -sS -X POST "$PYTEXAS_MARKETING_WEBHOOK" -H "Content-Type: application/json" -d "$PAYLOAD"'
```

where `PAYLOAD` is `{"content": "<message>"}`; `sops exec-env` keeps the decrypted URL out of shell history and files.

Message template (fill only the slots):

```text
<Month> meetup is booked!
* Date: <Weekday>, <Month> <Day> at 8:00 PM Central
* Talk: <Talk Title>
* Speaker: <Speaker Name>
* Card: <Canva design link>
* RSVP: https://pytexas.org/meetup/join
```

PROPOSED: the monthly message wording has not been used for a real announcement yet.
Confirm it with Mason on first use, then delete this paragraph.
