# Lessons Learned

## Recent
<!-- 10 most recent lessons, newest first -->
- Canva export URLs are signed and expire within hours; for Discord announcements attach the PNG to the webhook message (`files[0]` multipart) so the image outlives the link, and state the link's expiry next to it (2026-07-31)
- meetup.com shows "0 upcoming events" to WebFetch because listings render client-side; the raw HTML's `__NEXT_DATA__` Apollo cache has full event data. Use `scripts/scrape_local_meetups.py` in the meetup-update skill, and check for embedded JSON before declaring any Next.js site unscrapeable (2026-07-31)
- Mailchimp's v3 API cannot edit content of new-builder (`content_type: multichannel`) campaigns; `PUT /content` looks successful but forks the draft to a legacy template shell. Replicate + PATCH settings only; paste copy in the UI (2026-07-31)
- Don't verify an API write by GETting it back from the same API; it echoes your write. If the system of record is a UI (Mailchimp builder), the UI is the only honest check (2026-07-31)
- Mailchimp Marketing keys end in `-usNN`; Transactional (Mandrill) keys are a separate product and format. The Transactional MCP rejects Marketing keys with "Invalid API key" (2026-07-31)
- `sops set file '["KEY"]' '"value"'` adds a key to a sops dotenv without a decrypt/edit/re-encrypt round trip (2026-07-31)
- Run secret-bearing commands via `sops exec-env secrets/meetup.sops.env '...'` so keys never hit disk or the transcript in plaintext (2026-07-31)
- Replicated Mailchimp campaigns keep the source's subject line; June and July 2026 both went out stale. Always PATCH the subject after replicating (2026-07-31)

## Mailchimp
- Newsletter campaign anatomy: meetup section is an h1 block plus one paragraphs block; the other three sections (AI Nights, Foundation, Community) are static month to month (2026-07-31)

## Workflow
- The meetup-update skill's `references/newsletter.md` is the canonical newsletter playbook; follow it over memory or improvisation (2026-07-31)
