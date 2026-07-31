# Newsletter Workflow (Mailchimp)

The monthly newsletter is a Mailchimp campaign sent to the "PyTexas" audience.
The draft for the upcoming meetup month is created as part of the monthly update.
Mason reviews, pastes the meetup copy, and sends or schedules it himself.
Never send or schedule a campaign from this workflow; create drafts only.

## API Access

- **Base URL:** `https://us11.api.mailchimp.com/3.0/` (datacenter `us11`)
- **Auth:** API key stored in `secrets/meetup.sops.env` as `MAILCHIMP_API_KEY`, encrypted with sops + age
- **Audience:** "PyTexas" list, id `fa6aa40a2e`

Run API calls through `sops exec-env` so the key never lands in plaintext on disk or in the transcript:

```bash
sops exec-env secrets/meetup.sops.env \
  'curl -s -u "anystring:$MAILCHIMP_API_KEY" "https://us11.api.mailchimp.com/3.0/ping"'
```

Do not print the decrypted key. Do not commit decrypted output.

## Naming Conventions

- **Campaign title:** `PyTexas <Month> <Year> Newsletter`
- **Subject line:** `PyTexas Monthly <Month> <Year>` (or a `PyTexas Monthly: <highlights>` variant when there is conference news)
- **Preview text:** one line teasing the meetup talk

Always set the subject explicitly.
Replication carries the old subject forward: the June and July 2026 issues both went out with the stale subject "PyTexas Monthly April 2026".

## Step A: Check Whether This Month's Newsletter Exists

Look for a campaign titled `PyTexas <Month> <Year> Newsletter` for the upcoming meetup month:

```bash
sops exec-env secrets/meetup.sops.env \
  'curl -s -u "anystring:$MAILCHIMP_API_KEY" "https://us11.api.mailchimp.com/3.0/campaigns?count=20&sort_field=create_time&sort_dir=DESC&fields=campaigns.id,campaigns.status,campaigns.settings.title,campaigns.settings.subject_line"'
```

If it exists (any status), report its status and stop; do not modify an existing draft without being asked.

## Step B: Create It if Missing

1. Identify the most recent **sent** campaign titled `PyTexas ... Newsletter` (skip sponsor blasts and other one-offs).
2. Replicate it:

   ```bash
   sops exec-env secrets/meetup.sops.env \
     'curl -s -u "anystring:$MAILCHIMP_API_KEY" -X POST "https://us11.api.mailchimp.com/3.0/campaigns/<LAST_ID>/actions/replicate"'
   ```

3. Update the settings on the new campaign id:

   ```bash
   sops exec-env secrets/meetup.sops.env \
     'curl -s -u "anystring:$MAILCHIMP_API_KEY" -X PATCH "https://us11.api.mailchimp.com/3.0/campaigns/<NEW_ID>" \
       -H "Content-Type: application/json" \
       -d "{\"settings\":{\"title\":\"PyTexas <Month> <Year> Newsletter\",\"subject_line\":\"PyTexas Monthly <Month> <Year>\",\"preview_text\":\"<talk teaser>\"}}"'
   ```

4. Confirm the response shows `"status": "save"` and `"content_type": "multichannel"`.

## Hard Limit: Never Edit Content via the API

Newsletter campaigns are built in Mailchimp's new email builder (`content_type: multichannel`).
The v3 API **cannot** edit their content.
A `PUT /campaigns/{id}/content` appears to succeed (a GET echoes the HTML back) but the UI renders from the builder's internal document: the draft silently falls back to the legacy builder showing an unfilled template.
Confirmed empirically 2026-07-31.

**Never PUT `/content`.**
Instead, draft the meetup section copy in chat, formatted for Mason to paste into the builder (heading block + body paragraphs).

## Newsletter Structure

Sections in order; only the meetup announcement changes month to month:

1. Meetup announcement (h1 + paragraphs + "Join the Meetup" button, which always links to `https://pytexas.org/meetup/join`)
2. PyTexas AI Nights & Coffee Chats
3. Support the PyTexas Foundation
4. The PyTexas Community (social links)

## Meetup Section Copy Style

### Speaker Month (model: June 2026, campaign `065684fea1`)

- **Heading:** benefit-phrased, e.g. "Learn to become a better mentor at this month's Meetup"
- **Intro:** `Join us on M/D/YYYY at 8:00pm CST for our monthly PyTexas Meetup. <role/affiliation> <speaker name> joins us to <one-line topic hook>.`
- **Body:** the talk abstract, speaker's own words (first person is fine)
- **Closer:** `We'll see you in the Discord server for chat and the meetup!`

### Lightning Talks Month (model: July 2026, campaign `ad92f53315`)

- **Heading:** `Lightning Talks Meetup!`
- **Body:** pitch that anyone can speak for ~5 minutes on anything Python-adjacent, encourage first-time speakers, link the signup form, state that the form closes at noon the Friday before the meetup

## Reminders to Flag to Mason Each Month

1. Paste the drafted meetup copy into the two content blocks (heading and paragraphs) in the Mailchimp builder.
2. Check the hero image link at the top of the email (as of July 2026 it still pointed to `https://www.pytexas.org/2024`).
3. Verify the subject line says the current month before sending.
4. Send or schedule manually; historical sends go out on the 1st of the month at 9:15am Central.
