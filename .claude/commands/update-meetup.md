---
description: Fetch a meetup.com event page and run the monthly meetup update workflow.
---

Fetch the meetup.com event page at the following URL and extract the speaker and talk information:

$ARGUMENTS

Use WebFetch to retrieve the page content. Extract the following details:
- **Event date** (the date of the meetup)
- **Talk title**
- **Speaker name**
- **Talk description** (full description)
- **Speaker bio** (if available on the page)
- **Speaker headshot URL** (if available on the page)

After extracting this information, present it to the user for confirmation before proceeding.

Once confirmed, use the "meetup-update" skill to execute the full monthly update workflow:
1. Archive the current meetup from the homepage into a past meetup post
2. Add the new speaker to the authors file
3. Update the homepage with the new meetup details

If any required information is missing from the meetup.com page (e.g., speaker bio, headshot), ask the user to provide it before continuing with the update.
