# Run of Show Template

The fill-in content for the monthly run of show Google Doc.
This mirrors the Drive doc "Run of Show Template"; the Drive doc is the structural source of truth.
Fill only the `<angle bracket>` slots.
Slots marked TBD stay literal until meetup night.

```text
PyTexas Virtual Meetup - <Month> <Year>

# Schedule

- 7:30 - Join voice chat in #pre-and-post-meetup-chat
- 7:55 - Launch Discord stage and event and migrate people from chat to stage
- 8:00 - Meetup!
  - Welcome and Announcements
  - Main Talk - <Speaker Name>
  - Wrap up and drawing for door prize
- After - Join voice chat in #pre-and-post-meetup-chat

# Roles

- Host: TBD
- Moderators: TBD
- Winner: TBD

# Announcements

- Attendance Survey: <attendance form URL>
- Door Prize - A tech book up to $50
- Questions: <questions form URL, or "Just ask in chat tonight">
- Speak at this very PyTexas Virtual Meetup! The CFP is open at https://www.pytexas.org/meetup/
- <current announcements: conference dates, ticket sales, grants, and similar>

# Links

- Attendance: <attendance form URL>
- Attendance Answers: <responses sheet URL, placeholder until the sheet exists>

# Speaker Data

### Talk

#### <Talk Title> - <Speaker Name>

<Full talk description>

### Bio: <Full speaker bio>

# Upcoming Meetups

Pull up https://www.pytexas.org/meetup/local-meetups/ for this.

| Meetup | Date | Location | Area |
| ------ | ---- | -------- | ---- |
| TBD    |      |          |      |

If you know of other groups, add them!

## Next month

<Next meetup date and, if booked, speaker and talk>

Useful links

- Meetup CFP: https://forms.gle/a9WrW7wJSkPCCG437
- PyTexas Foundation Site: https://pytexas.org
- PyTexas Conference Site: https://www.pytexas.org/<conference year>
- PyTexas Meetup Site: https://pytexas.org/meetup

Polls

<Optional: one or two audience polls with lettered options>

# Drawing Winner
```

For July lightning talks, the Speaker Data section is the ordered speaker list instead of a single talk, and the Schedule's Main Talk line reads "Lightning Talks".

## Research to Fill the Doc

The run of show is not a pure fill-in; three sections need research at creation time.
This research flow has not had a live run yet; expect to refine it the first month it executes.

### Upcoming Meetups Table

1. Read `docs/local-meetups.md` in this repo (the source behind https://www.pytexas.org/meetup/local-meetups/); it lists each group, its meetup.com URL, and an Active or Inactive marker.
2. For each Active group, fetch its meetup.com page and pull the next scheduled event: date, time, and location.
3. Fill the table rows (Meetup, Date, Location, Area) and note any active group with nothing on the calendar.

### Announcements

- Recurring items: the attendance survey link, the door prize (a tech book up to $50), the questions form or "just ask in chat", and the meetup CFP plug.
- Time-sensitive items: pull current conference news from pytexas.org (CFP windows, ticket sales, grant deadlines, schedule announcements) and check the previous month's run of show for items still running.
- Ask Mason for anything else before finalizing; announcements are the section he edits most.

### Next Month

Use the booked speaker and talk for the following month from the CFP sheet and email threads.
If nothing is booked yet, list just the date.

### Polls (Optional)

Propose one or two multiple-choice polls themed to the talk topic, matching the style of past docs.
Mason approves or cuts them.
