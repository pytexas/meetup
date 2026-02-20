---
name: Monthly Meetup Update
description: >-
  This skill should be used when the user asks to "update the meetup",
  "do the monthly update", "archive the meetup", "add the next meetup",
  "update for [month] meetup", "set up the new meetup", "prepare next
  month's meetup", or provides speaker submission data for an upcoming
  meetup. Guides the complete monthly transition workflow for the PyTexas
  Meetup website including archiving the current meetup, adding the new
  speaker, and updating the homepage.
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

The user typically provides raw speaker submission data containing:

- Speaker name and pronouns
- Email
- Talk title and description
- Headshot link (usually Google Drive)
- Speaker bio

## Workflow

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
- The RSVP link is always `https://pytexas.org/meetup/join` — no per-event update needed
- Update the headshot image path and speaker bio

See `references/file-formats.md` for the exact markdown format.

### Step 4: Flag Manual Steps

After completing the automated changes, remind the user of one manual task:

1. **Speaker headshot**: Download from the provided link and save to `docs/assets/images/<name>.<ext>`

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

## Additional Resources

### Reference Files

- **`references/file-formats.md`** - Exact file format templates for all three files that get modified
