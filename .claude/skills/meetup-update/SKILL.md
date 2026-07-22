---
name: Monthly Meetup Update
description: >-
  This skill should be used when the user asks to "update the meetup",
  "do the monthly update", "schedule the monthly meetup", "archive the
  meetup", "add the next meetup", "update for [month] meetup", "set up
  the new meetup", "prepare next month's meetup", provides speaker
  submission data for an upcoming meetup, provides a meetup.com event
  URL, or asks to pull a speaker's submission from the Google Form /
  CFP responses spreadsheet. Also available via the `/update-meetup`
  command with a meetup.com URL. Runs the full monthly meetup setup:
  pulling the speaker from the CFP sheet, updating the website,
  creating the Drive month folder with the run of show and attendance
  form, creating the Canva promo card, notifying the Discord marketing
  channel, and flagging the event listings that stay manual.
---

# Monthly Meetup Update

This skill runs the full monthly setup for the next PyTexas Meetup.
It mirrors the recurring Todoist task "Schedule Monthly Meetup" (every 2nd Wednesday, in the PyTexas project), which is the checklist of record.

## Overview

The Todoist subtasks and how this skill handles each:

1. **Update Meetup Website** - automated here: archive the held meetup, add the speaker to authors, update the homepage, open a PR
2. **Create Canva Card** - attempted via the Canva MCP; flagged with the design's edit link if editing fails
3. **Send Social Media Assets to Kassandra** - handled by posting to the Discord marketing channel webhook
4. **Create Discord Event** - manual, flagged at the end
5. **Create Network Event on Meetup** - manual, flagged at the end
6. **Create Event on Non-network meetups (MKE)** - manual, flagged at the end

Beyond the Todoist list, the skill also creates the meetup-night materials in Drive: the month folder, the run of show doc, and the attendance form.

Speaker data always comes from the Google MCP first (Drive for the CFP sheet, Gmail for the booked date).
If Todoist is connected, re-read the subtasks of "Schedule Monthly Meetup" at the start in case the checklist has changed, and follow the live list over the one above.

## Template Policy

Every artifact this skill produces is template-driven.
Use the reference template verbatim and fill only the marked slots; never rewrite, paraphrase, or improvise the template prose.
The outreach email, run of show, attendance form, Canva card, and Kassandra email each have a reference file listed at the bottom.
If Mason changes an artifact's wording, update its template file so the next run produces the new exact version.

## Input Data

Always pull from the Google MCP first.
The other input options are fallbacks for when Drive is unavailable or the user hands over data directly.

### Primary Source: CFP Responses Spreadsheet (Google Drive)

Speaker submissions land in the "PyTexas Meetup CFP (Responses)" Google Sheet.
Search Drive for it by title; there is an older sheet with the same name from 2024, so pick the one with recent timestamps.
Relevant columns: Name, About you (bio), Speaker Photo, Presentation Title, Presentation Description, Estimated Presentation Length, Acked, Comments.

- Acked TRUE means Mason has already contacted the speaker.
- Acked FALSE with a dismissive comment (e.g. "Not enough to go off of") means the submission was passed on; do not book or contact without asking.
- Early rows are form tests from Josh Schneider and Mason; ignore them.
- A speaker may submit more than once; the latest row usually supersedes earlier ones, but confirm which talk they actually gave or will give.

The July lightning talks have their own sheet (e.g. "PyTexas July 2026 Lightning Talks (Responses)") with a Speaker Order tab.

### Fallback A: Meetup.com Event URL

When given a meetup.com URL (or invoked via `/update-meetup <url>`), use WebFetch to retrieve
the event page and extract: event date, talk title, speaker name, talk description, speaker bio,
and speaker headshot URL. Present the extracted data to the user for confirmation before proceeding.
If any required fields are missing from the page, ask the user to provide them.

### Fallback B: Raw Speaker Submission Data

The user provides speaker submission data directly containing:

- Speaker name and pronouns
- Email
- Talk title and description
- Headshot link (usually Google Drive)
- Speaker bio

## Confirming the Speaker's Date

The CFP submission does not carry a meetup date. Never assume the speaker is booked for the next open month.

Mason emails each accepted speaker (subject "Speak at PyTexas Meetup") offering the open first-Tuesday dates and asking them to pick two; the booked date is settled in that thread.
Before putting a speaker on the homepage, search Gmail for the thread and confirm which date was locked in.
If the thread is ambiguous or unanswered, ask Mason instead of guessing.

Also check the thread for corrections to the form data, such as a different preferred contact email.

## Workflow

### Step 1: Pull Speaker Data From Google

This is always the first step.
Find the booked speaker's row in the CFP responses sheet (see Primary Source above), then confirm their locked-in date from the Gmail thread (see Confirming the Speaker's Date).
Carry forward the talk title, description, bio, headshot source, and any corrected contact email.

### Step 2: Sync With Main

The site may be several months behind, and main may have moved since the local checkout.
Fetch origin, start a feature branch from up-to-date main, and check which meetups are already archived in `docs/past_meetups/posts/` before deciding what to archive.
Never commit to main; Mason merges PRs himself.

### Step 3: Archive the Current Meetup

Create a new file at `docs/past_meetups/posts/YYYY-MM-DD.md` where the date is the date
of the meetup being archived (the one currently on the homepage).

Copy the talk title, description, speaker bio, and headshot reference from `docs/index.md`
into the new post file. Follow the format documented in `references/file-formats.md`.

### Step 4: Add the New Speaker to Authors

Edit `docs/past_meetups/.authors.yml` to add a new entry for the incoming speaker.

- Use a lowercase, no-spaces key derived from the speaker's name (e.g., `dippukumarsingh`)
- Write a concise description (2-3 sentences) based on the speaker's bio
- Set the avatar path to `assets/images/<name>.<ext>` matching the headshot filename

See `references/file-formats.md` for the exact YAML format.

### Step 5: Update the Homepage

Edit `docs/index.md` to replace the current meetup section with the new month's details.

- Update the heading to the new month and date (meetups are the **first Tuesday** of the month)
- Replace the talk title, speaker name, and description
- The RSVP link is always `https://pytexas.org/meetup/join`; no per-event update needed
- Update the headshot image path and speaker bio

See `references/file-formats.md` for the exact markdown format.

### Step 6: Flag the Headshot If Missing

After completing the website changes, remind the user of one manual task:

1. **Speaker headshot**: Download from the provided link and save to `docs/assets/images/<name>.<ext>`

The Speaker Photo field sometimes says to email the speaker for the file instead of giving a URL.
In that case Mason requests it over email; the site references the image path before the file exists, so `mkdocs build --strict` (and CI) fails until the headshot lands.
If the PR must wait on the headshot or an earlier month's speaker, mark it as a draft.

### Step 7: Create the Drive Artifacts

Create the month folder, run of show doc, and attendance form in Google Drive.
Follow `references/drive-artifacts.md` for the folder layout, template locations, and copy procedure, and `references/run-of-show.md` for the fill-in content.
Filling the run of show includes research (the local meetups table, current announcements, next month's teaser); follow the Research section of `references/run-of-show.md`.
Roles stay as placeholders until meetup night.

### Step 8: Create the Canva Card

The promo cards live in one Canva deck per season (September through August), one page per month.
Follow `references/canva-cards.md` for picking or creating the right deck and adding the page.
If the editing tools cannot make the change cleanly, stop and give Mason the design's edit URL with the exact text to place; do not leave a half-edited page.

### Step 9: Notify the Marketing Channel

Post the month's promo details to the marketing channel in the PyTexas Discord through the webhook, following `references/discord-webhook.md`.
Fire it only after the Canva card exists so the message can link it.
If the webhook URL is not configured, flag the notification as a manual step instead.

### Step 10: Flag the Event Listings

These have no MCP access and stay manual. List them for Mason at the end of the run:

1. **Create Discord Event** in the PyTexas Discord
2. **Create Network Event on Meetup** (meetup.com)
3. **Create Event on Non-network meetups** (MKE)

Meetup.com event creation is automatable through their GraphQL API once Mason obtains OAuth credentials (requested through the Meetup Pro admin account).
Until those credentials exist and an integration is set up, treat it as manual; when they do, codify it here.

### Step 11: Report Against the Todoist Checklist

Finish by reporting each "Schedule Monthly Meetup" subtask as done, drafted awaiting Mason's review, or still manual.
Do not check off subtasks in Todoist without Mason's confirmation; the website subtask in particular is not done until the PR merges and the headshot lands.

## Determining the Meetup Date

PyTexas meetups are held on the **first Tuesday of each month**. Calculate the correct date
for the upcoming month. For example:

- If the 1st of the month is a Sunday, the first Tuesday is the 3rd
- If the 1st of the month is a Wednesday, the first Tuesday is the 7th

## Content Guidelines

### Talk Description on Homepage

Use only the first paragraph or a concise summary of the talk description on the homepage.
The full description goes in the past meetup archive post when it is eventually archived.

### Speaker Bio

- On the homepage (`index.md`): Use the full bio, italicized with **`_underscores_`**
- In past meetup posts: Use the full bio, italicized with **`*asterisks*`**
- In `.authors.yml`: Use a condensed 2-3 sentence version

### Categories for Past Meetup Posts

Choose 2-4 relevant categories based on the talk topic. Common categories include:
Python, AI, LLMs, Data, Web, DevOps, Testing, Tooling, Code Quality, Security,
Machine Learning, Cloud, Automation.

## Edge Cases

If there is no meetup for a given month (e.g., conference month, holiday skip), ask the user
for guidance on what to display on the homepage instead of the typical upcoming meetup section.

### July Lightning Talks

July is the annual "Summer of Lightning Talks" meetup; there is no single speaker.

- The homepage section has no speaker or headshot; it links the RSVP page and the talk sign-up form.
- The archive post is titled "Summer of Lightning Talks", authored by `masonegger`, and lists each speaker and talk title as bullets after the `<!-- more -->` tag.
  Match the prior year's post (e.g. `docs/past_meetups/posts/2025-07-01.md`).
- Pull the speaker list and order from that year's lightning talks response sheet in Drive.

### Speaker Booked for a Later Month

A speaker may lock in a month other than the next open one, leaving nearer months without a speaker.
Put the speaker in their confirmed month, ask Mason what to do about the open months, and mark the PR as a draft until they are filled.

## Speaker Outreach

When months need speakers, un-acked CFP submissions are the candidate pool.
Mason sends each candidate the standard offer email; draft (never send) these in Gmail using `references/outreach-email.md`, listing only the still-open dates.
After drafting, remind Mason that Gmail rewrites bare URLs in API-created drafts into `google.com/url` redirect wrappers, so he should check the Discord link in the compose window before sending.

## Additional Resources

### Reference Files

- **`references/file-formats.md`** - Exact file format templates for the three website files that get modified
- **`references/outreach-email.md`** - Exact template for the speaker date-offer email
- **`references/drive-artifacts.md`** - Drive folder layout and procedure for the run of show and attendance form
- **`references/run-of-show.md`** - Exact fill-in template for the run of show doc
- **`references/canva-cards.md`** - Canva season deck rules, naming, and card procedure
- **`references/discord-webhook.md`** - Marketing channel webhook setup, payload, and message template (proposed, pending Mason's approval)
