---
name: Monthly Meetup Update
description: >-
  This skill should be used when the user asks to "update the meetup",
  "do the monthly update", "archive the meetup", "add the next meetup",
  "update for [month] meetup", "set up the new meetup", "prepare next
  month's meetup", provides speaker submission data for an upcoming
  meetup, provides a meetup.com event URL, or asks to pull a speaker's
  submission from the Google Form / CFP responses spreadsheet. Also
  available via the `/update-meetup` command with a meetup.com URL.
  Guides the complete monthly transition workflow for the PyTexas
  Meetup website including archiving the current meetup, adding the
  new speaker, and updating the homepage.
---

# Monthly Meetup Update

This skill handles the recurring monthly workflow for transitioning the PyTexas Meetup website
from the current month's meetup to the next month's meetup.

## Overview

Each month, the website needs three updates:

1. **Archive** the current meetup as a past meetup blog post
2. **Add** the new speaker to the authors file
3. **Update** the homepage with the upcoming meetup details

Additionally, one manual step is flagged for the user:

- Download and save the speaker's headshot image

## Input Data

Input can come from three sources:

### Option A: CFP Responses Spreadsheet (Google Drive)

Speaker submissions land in the "PyTexas Meetup CFP (Responses)" Google Sheet.
Search Drive for it by title; there is an older sheet with the same name from 2024, so pick the one with recent timestamps.
Relevant columns: Name, About you (bio), Speaker Photo, Presentation Title, Presentation Description, Estimated Presentation Length, Acked, Comments.

- Acked TRUE means Mason has already contacted the speaker.
- Acked FALSE with a dismissive comment (e.g. "Not enough to go off of") means the submission was passed on; do not book or contact without asking.
- Early rows are form tests from Josh Schneider and Mason; ignore them.
- A speaker may submit more than once; the latest row usually supersedes earlier ones, but confirm which talk they actually gave or will give.

The July lightning talks have their own sheet (e.g. "PyTexas July 2026 Lightning Talks (Responses)") with a Speaker Order tab.

### Option B: Meetup.com Event URL

When given a meetup.com URL (or invoked via `/update-meetup <url>`), use WebFetch to retrieve
the event page and extract: event date, talk title, speaker name, talk description, speaker bio,
and speaker headshot URL. Present the extracted data to the user for confirmation before proceeding.
If any required fields are missing from the page, ask the user to provide them.

### Option C: Raw Speaker Submission Data

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

### Step 0: Sync With Main

The site may be several months behind, and main may have moved since the local checkout.
Fetch origin, start a feature branch from up-to-date main, and check which meetups are already archived in `docs/past_meetups/posts/` before deciding what to archive.
Never commit to main; Mason merges PRs himself.

### Step 1: Archive the Current Meetup

Create a new file at `docs/past_meetups/posts/YYYY-MM-DD.md` where the date is the date
of the meetup being archived (the one currently on the homepage).

Copy the talk title, description, speaker bio, and headshot reference from `docs/index.md`
into the new post file. Follow the format documented in `references/file-formats.md`.

### Step 2: Add the New Speaker to Authors

Edit `docs/past_meetups/.authors.yml` to add a new entry for the incoming speaker.

- Use a lowercase, no-spaces key derived from the speaker's name (e.g., `dippukumarsingh`)
- Write a concise description (2-3 sentences) based on the speaker's bio
- Set the avatar path to `assets/images/<name>.<ext>` matching the headshot filename

See `references/file-formats.md` for the exact YAML format.

### Step 3: Update the Homepage

Edit `docs/index.md` to replace the current meetup section with the new month's details.

- Update the heading to the new month and date (meetups are the **first Tuesday** of the month)
- Replace the talk title, speaker name, and description
- The RSVP link is always `https://pytexas.org/meetup/join`; no per-event update needed
- Update the headshot image path and speaker bio

See `references/file-formats.md` for the exact markdown format.

### Step 4: Flag Manual Steps

After completing the automated changes, remind the user of one manual task:

1. **Speaker headshot**: Download from the provided link and save to `docs/assets/images/<name>.<ext>`

The Speaker Photo field sometimes says to email the speaker for the file instead of giving a URL.
In that case Mason requests it over email; the site references the image path before the file exists, so `mkdocs build --strict` (and CI) fails until the headshot lands.
If the PR must wait on the headshot or an earlier month's speaker, mark it as a draft.

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

- **`references/file-formats.md`** - Exact file format templates for all three files that get modified
- **`references/outreach-email.md`** - Template for the speaker date-offer email
