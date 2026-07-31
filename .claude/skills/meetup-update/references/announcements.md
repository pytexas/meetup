# Discord Announcements (Marketing and Organizers Channels)

After the monthly setup is complete, two Discord channels get an announcement via webhooks stored in `secrets/meetup.sops.env`:

- `PYTEXAS_MARKETING_WEBHOOK`: the marketing channel; audience prepares social posts
- `PYTEXAS_MEETUP_WEBHOOK`: the meetup organizers channel; audience runs the meetup

Send with `scripts/send_discord_announcement.py` (never hand-roll the curl):

```bash
sops exec-env secrets/meetup.sops.env \
  './.claude/skills/meetup-update/scripts/send_discord_announcement.py marketing marketing.json --image card.png'
sops exec-env secrets/meetup.sops.env \
  './.claude/skills/meetup-update/scripts/send_discord_announcement.py organizers organizers.json --image card.png'
```

The payload file is Discord message JSON: `{"content": "..."}`, under 2000 characters.

## Card Image Handling

The promo card lives in the "2026 Meetup Banners" Canva deck (design id `DAGv-Ktk4IM`, share link <https://www.canva.com/d/aiHt9RXm1DY_dI7>), one page per month.
Canva export URLs are signed and expire within hours, so always attach the PNG to the message (`--image`) in addition to quoting the download link; the attachment persists in Discord after the link dies.
Always state the link's expiry time next to it and note that re-export happens from the deck.

## Message Templates

Marketing (bullet list, one item per line):

```
August 2026 meetup: everything is live!
* Date: Tuesday, <Month> <D> at 8:00 PM Central
* Talk: <Title> - <Speaker>
* Promo blurb: <2-3 sentence hook from the talk description>
* Card (Canva): <deck share link> (page N of 2026 Meetup Banners)
* Card image: attached below; direct download (link expires <time>, re-export from the deck after that): <signed URL>
* Run of Show: <Google Doc link>
* Attendance form: <forms.gle link>
* Questions: in chat tonight
* Meetup.com event: <canonical event URL> (cross-posted to all network groups)
* Discord event: <discord.com/events/... link>
* RSVP: https://pytexas.org/meetup/join
```

Organizers (shorter; logistics only):

```
<Month> <Year> meetup setup is done.
* Tuesday, <Month> <D> at 8:00 PM Central: <Title> - <Speaker>
* Run of Show: <Google Doc link>
* Card (Canva): <deck share link> (page N); image attached, direct download (link expires <time>): <signed URL>
* Discord event: <link>
* Meetup.com event: <link>
* Attendance form: <forms.gle link>
* Website PR: <link> (merged | pending merge)
```

If any step is still manual/incomplete, end the organizers message with a `Still manual:` line listing them; drop the line entirely once everything is done.

## Gotchas Learned the Hard Way

- The attendance form link must be the published responder link (forms.gle or `/d/e/...`), never the `/d/<id>/viewform` edit-ID URL, which only works for the owner. Verify it with an unauthenticated fetch before sending.
- The canonical meetup.com event lives on the PyTexas Virtual Meetup group (<https://www.meetup.com/pytexas-virtual-meetup-austin/>); the copies on other network groups' pages are cross-posts. Use `scripts/scrape_local_meetups.py` techniques (or that group's events page) to find it.
- Webhook success with `?wait=true` returns HTTP 200 and the created message JSON; check the message id and attachment list rather than assuming delivery.
