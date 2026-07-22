# Drive Artifacts: Month Folder, Run of Show, Attendance Form

Every meetup gets a folder in Google Drive holding its run of show doc, attendance form, and the response sheets that accumulate around it.
Create these at setup time; slots that depend on meetup night (roles, announcements, the local meetups table) stay as placeholders until then.

Find everything by title search, never by hardcoded file ID (this repo is public).

## Folder Layout

```text
<Meetups root>/
  <YYYY>/                 year folder, e.g. "2026"
    <YYYY-MM-DD>/         month folder named for the meetup date, e.g. "2026-02-03"
      Run of Show <YYYY-MM-DD>
      PyTexas Virtual Meetup Attendance <YYYY-MM-DD>          (Google Form)
      PyTexas Virtual Meetup Attendance <YYYY-MM-DD> (Responses)
      Questions for <Speaker>                                  (optional Google Form)
      Questions for <Speaker> (Responses)
```

## Creating the Month Folder

1. Search Drive for the year folder (title equals the four-digit year). Its parent is the meetups root.
2. If the year folder does not exist yet (January), create it there first.
3. Create the month folder inside it, titled `YYYY-MM-DD` (the meetup date).

## Creating the Run of Show

1. Search Drive for the doc titled "Run of Show Template".
2. Copy it into the month folder with the title `Run of Show YYYY-MM-DD`.
3. Fill the slots per `run-of-show.md`, which mirrors the template's structure.
   Fill what is known at setup time (month, speaker, talk, bio, attendance links); leave roles and announcements as placeholders.

If the Drive template has drifted from `run-of-show.md`, the Drive template wins for structure; update `run-of-show.md` to match and tell Mason.

## Creating the Attendance Form

Google Forms cannot be authored through the Drive MCP, but they can be copied.

1. Search Drive for the form titled "PyTexas Meetup Attendance <DATE>" (it lives in the "Attendance Forms Template" folder).
2. Copy it into the month folder with the title `PyTexas Virtual Meetup Attendance YYYY-MM-DD`.
3. Put the copy's full form URL in the run of show under Announcements and Links.

Caveats to flag to Mason every time:

- The copied form's questions come from the template (Name, closest Texas region). Nothing to edit unless the questions changed.
- The response spreadsheet does not exist until someone opens the form's Responses tab; the "Attendance Answers" link in the run of show stays a placeholder until then.
- The short `forms.gle` link can only be generated from the form's Send dialog in the browser. The run of show gets the full URL; Mason swaps in the short link if he wants one.
