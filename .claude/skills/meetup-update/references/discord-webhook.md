# Marketing Channel Webhook

The monthly promo notification goes to the marketing channel in the PyTexas Discord via a webhook.
There is no emailed social media asset handoff; this post is the handoff.

## Configuration

The webhook URL is a secret.
Never commit it to this repo; read it from the `PYTEXAS_MARKETING_WEBHOOK` environment variable.
If the variable is unset, skip the post, flag it as manual, and remind Mason how to set it up: in the marketing channel, Channel Settings, Integrations, Webhooks, create one and export its URL in the shell profile or Claude Code settings env.

## Posting

Fire only after the Canva card exists so the link works.
Show Mason the exact message in the run summary.

```bash
curl -sS -X POST "$PYTEXAS_MARKETING_WEBHOOK" \
  -H 'Content-Type: application/json' \
  -d '{"content": "<message>"}'
```

Message template (fill only the slots):

```text
<Month> meetup is booked!
* Date: <Weekday>, <Month> <Day> at 8:00 PM Central
* Talk: <Talk Title>
* Speaker: <Speaker Name>
* Card: <Canva design link>
* RSVP: https://pytexas.org/meetup/join
```

PROPOSED: the message wording has not been used yet and no webhook is configured.
Confirm both with Mason on first use, then delete this paragraph.
