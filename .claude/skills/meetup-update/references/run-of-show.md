# Run of Show Template

The fill-in content for the monthly run of show Google Doc.
Build the doc as markdown and upload it with conversion to a native Google Doc; `drive-artifacts.md` has the upload mechanics and why not HTML.
Headings are `##`, the upcoming-meetups table is a pipe table (its first row becomes a bold header), and a literal placeholder like `<DATE>` must be written `&lt;DATE&gt;` so import does not drop it as an HTML tag.
Fill the `<angle bracket>` slots; leave the `FILL_ME_IN` markers and the HUMAN REQUIRED TASKS list for the human running the night.

```text
# PyTexas Virtual Meetup - <Month> <Year>

## HUMAN REQUIRED TASKS

These cannot be done through the API. Both form edit links are right here so you are not hunting for them.

- Attendance form (edit): <attendance form edit URL>
- Questions form (edit): <questions form edit URL>

1. **PUBLISH BOTH FORMS.** Open each form above, click Publish/Send, then paste the forms.gle responder links into the Links and Announcements sections below.
2. **UPDATE EACH FORM'S INTERNAL TITLE AND DESCRIPTION.** The attendance form still reads "&lt;DATE&gt;" and the questions form still reads "&lt;SPEAKER&gt;" inside the form itself. Edit the on-screen title and description to the meetup date and the speaker name. The Drive file names are already correct; only the form content needs it.
3. **MAKE THE RESPONSE SHEETS.** In each form's Responses tab, click Link to Sheets, then paste each sheet link into the Links section.
4. **FILL IN THE ROLES.** Host, Moderators, and Winner below are marked FILL_ME_IN.

## Schedule

- 7:30 - Join voice chat in #pre-and-post-meetup-chat
- 7:55 - Launch Discord stage and event and migrate people from chat to stage
- 8:00 - Meetup!
    - Welcome and Announcements
    - Main Talk - <Speaker Name>
    - Wrap up and drawing for door prize
- After - Join voice chat in #pre-and-post-meetup-chat

## Roles

- Host: **FILL_ME_IN**
- Moderators: **FILL_ME_IN**
- Winner: **FILL_ME_IN** (filled in during the drawing)

## Announcements

- Attendance Survey: **PUBLISH THE FORM** (see Human Required Tasks), then paste the responder link here
- Door Prize - A tech book up to $50
- Questions form: **PUBLISH THE FORM** (see Human Required Tasks), then paste the responder link here, or just ask in chat tonight
- Speak at this very PyTexas Virtual Meetup! The CFP is open at https://www.pytexas.org/meetup/
- <current announcements: conference dates, ticket sales, grants, and similar>

## Links

- Attendance form (edit): <attendance form edit URL>
- Attendance form (responder): **FILL_ME_IN** - publish to generate
- Attendance answers (sheet): **FILL_ME_IN** - create via Responses > Link to Sheets
- Questions form (edit): <questions form edit URL>
- Questions form (responder): **FILL_ME_IN** - publish to generate
- Questions answers (sheet): **FILL_ME_IN** - create via Responses > Link to Sheets

## Speaker Data

### Talk

#### <Talk Title> - <Speaker Name>

<Full talk description>

### Bio

<Full speaker bio>

## Upcoming Meetups

<one-line note on when the table was checked, plus the cross-post caveat>

| Meetup | Date | Location | Area |
| --- | --- | --- | --- |
| <group> | <next event date and time, or "No <Month> event listed"> | <location> | <area> |

If you know of other groups, add them!

### Next month

<Next meetup date and, if booked, speaker and talk>

Useful links

- Meetup CFP: https://forms.gle/a9WrW7wJSkPCCG437
- PyTexas Foundation Site: https://pytexas.org
- PyTexas Conference Site: https://www.pytexas.org/<conference year>
- PyTexas Meetup Site: https://pytexas.org/meetup

Polls

Poll 1: <optional audience poll themed to the talk, with lettered options>

## Drawing Winner
```

For July lightning talks, the Speaker Data section is the ordered speaker list instead of a single talk, and the Schedule's Main Talk line reads "Lightning Talks".

## Research to Fill the Doc

The run of show is not a pure fill-in; three sections need research at creation time.

### Upcoming Meetups Table

1. Read `docs/local-meetups.md` in this repo (the source behind https://www.pytexas.org/meetup/local-meetups/); it lists each group, its meetup.com URL, and an Active or Inactive marker.
2. For each Active group, get its next scheduled event (date, time, location) with `scripts/scrape_local_meetups.py`; see `references/local-meetups.md`. Do not use WebFetch on meetup.com.
3. Fill the table rows (Meetup, Date, Location, Area) and mark any active group with nothing on the calendar as "No <Month> event listed".

### Announcements

- Recurring items: the attendance survey link, the door prize (a tech book up to $50), the questions form (or "just ask in chat"), and the meetup CFP plug.
- Time-sensitive items: pull current conference news from pytexas.org (CFP windows, ticket sales, grant deadlines, schedule announcements) and check the previous month's run of show for items still running.
- Ask Mason for anything else before finalizing; announcements are the section he edits most.

### Next Month

Use the booked speaker and talk for the following month from the CFP sheet and email threads.
If nothing is booked yet, list just the date.

### Polls (Optional)

Propose one or two multiple-choice polls themed to the talk topic, matching the style of past docs.
Mason approves or cuts them.
