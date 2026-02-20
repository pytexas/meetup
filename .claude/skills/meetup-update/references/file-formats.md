# File Format Reference for Monthly Meetup Update

This document contains the exact templates for the three files modified during each
monthly meetup update.

## Past Meetup Post

**Location:** `docs/past_meetups/posts/YYYY-MM-DD.md`

The date in the filename is the date the meetup was held (first Tuesday of that month).

```markdown
---
title: "Talk Title Here"
description: "One sentence summary of the talk."
date: YYYY-MM-DD
categories:
    - Category1
    - Category2
authors:
    - authorkey
---

# [Month] [Year] Meetup

[Full talk description paragraph(s)]

<!-- more -->

![Speaker Name Headshot](../../assets/images/speaker.jpg){: style="height:150px;width:150px" align=left}

*[Full speaker bio]*
```

### Key Details

- The `title` field is the talk title
- The `description` field is a brief one-sentence summary
- The `date` field matches the filename date
- Categories are indented with 4 spaces under `categories:`
- The author key must match the key used in `.authors.yml`
- The `<!-- more -->` tag separates the excerpt from full content
- The headshot path uses `../../assets/images/` (relative from posts directory)
- The bio uses `*asterisks*` for italics

## Authors File

**Location:** `docs/past_meetups/.authors.yml`

New entries are appended at the end of the file, inside the top-level `authors:` mapping.

```yaml
  speakername:
    name: Full Speaker Name
    description: Condensed 2-3 sentence bio focusing on role, expertise, and notable achievements.
    avatar: assets/images/speaker.jpg
```

### Key Details

- The key is lowercase with no spaces or special characters
- Indentation is 2 spaces for the key, 4 spaces for the fields
- The `avatar` path is relative to `docs/` (no leading `../../`)
- Keep the description concise: role + key expertise + 1-2 distinguishing facts

## Homepage Upcoming Meetup Section

**Location:** `docs/index.md`

Replace everything under `## Upcoming PyTexas Meetups` through the end of the speaker bio.

```markdown
## Upcoming PyTexas Meetups

### [Month] Meetup - [Month] [Day], [Year]

**[Talk Title]** - [Speaker Name]

[Talk description - first paragraph or concise summary]

[RSVP Here :fontawesome-solid-ticket:](https://pytexas.org/meetup/join){ .md-button .md-button--primary }

![Speaker Name Headshot](assets/images/speaker.jpg){: style="height:150px;width:150px" align=left}

_[Full speaker bio]_
```

### Key Details

- The headshot path uses `assets/images/` (relative from docs root)
- The RSVP link always points to `https://pytexas.org/meetup/join` — no per-event update needed
- The bio uses `_underscores_` for italics (different from past meetup posts)
- The image dimensions may vary; default is `height:150px;width:150px` but the user may adjust
- There is a blank line after the closing bio underscore

## Speaker Headshot

**Location:** `docs/assets/images/<name>.<ext>`

- Use a short, lowercase filename derived from the speaker's name
- Common extensions: `.jpg`, `.jpeg`, `.png`
- The user must manually download the image and place it here
