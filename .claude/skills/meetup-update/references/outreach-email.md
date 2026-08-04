# Speaker Outreach Email Template

The standard email Mason sends to accepted CFP submitters to offer meetup dates.
Create these as Gmail drafts for Mason to review and send; never send directly.

- To: the speaker's email from the CFP sheet (or their corrected contact email if they gave one)
- Cc: meetup@pytexas.org
- Subject: Speak at PyTexas Meetup

Replace `<First Name>` and list only the first-Tuesday dates that are still open (no booked speaker, not yet passed).

```text
Hey <First Name>,

Thanks for reaching out! We'd love to have you speak at our virtual meetup. Currently we are looking for speakers for the following dates:
* <Month> <Day>
* <Month> <Day>
* <Month> <Day>

Can you select two dates and send me your preference? Then can you make sure you've joined the PyTexas Discord (https://discord.gg/pytexas) and when you do, ping me so I can give you the proper permissions.

Thank you and we look forward to your presentation!

Mason

---
Mason Egger
PyTexas Foundation - President
PyTexas Conference - Conference Chair
PyTexas Meetup - Organizer
Python Software Foundation Fellow
```

Known issue: Gmail rewrites bare URLs in API-created drafts into `google.com/url?q=...` redirect wrappers.
The wrapped link still redirects correctly but looks mangled.
Providing an HTML body with an anchor tag does not prevent the rewrite in the stored plaintext, so after drafting, tell Mason to verify the Discord link in the compose window and retype it there if needed.

The speaker's reply names their two preferred dates; Mason picks one and that becomes the booked month.
Record the outcome by flipping the row's Acked column in the CFP sheet.
