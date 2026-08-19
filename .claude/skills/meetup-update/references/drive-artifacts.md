# Drive Artifacts: Month Folder, Run of Show, Attendance and Questions Forms

Every meetup gets a folder in Google Drive holding its run of show doc, its attendance and questions forms, and the response sheets that accumulate around them.
Create these at setup time; slots that depend on meetup night (roles, announcements, the local meetups table) stay as placeholders until then.

Find everything by title search, never by hardcoded file ID (this repo is public).

## Verify the Google Account First

The Drive MCP can silently reconnect to the wrong Google account (a personal one instead of the PyTexas account), and the failure looks like data loss: searches return empty, `get_file_metadata` on a known ID returns "not found", and `create_file` into a real folder returns "entity not found".
Before creating or copying anything, confirm the active account is PyTexas.
Every meetup-Drive file the MCP returns should carry `ouid=113545413620274301995` in its `viewUrl`, and `list_recent_files` should show PyTexas files rather than unrelated personal ones.
If it shows the wrong account, stop and ask Mason to reconnect the connector to the PyTexas Google account before continuing.

## Folder Layout

```text
<Meetups root>/
  <YYYY>/                 year folder, e.g. "2026"
    <YYYY-MM-DD>/         month folder named for the meetup date, e.g. "2026-02-03"
      Run of Show <YYYY-MM-DD>
      PyTexas Virtual Meetup Attendance <YYYY-MM-DD>          (Google Form)
      PyTexas Virtual Meetup Attendance <YYYY-MM-DD> (Responses)
      Questions for <Speaker>                                 (Google Form)
      Questions for <Speaker> (Responses)
```

The form templates live in the "Meetup Forms Template" folder (search for it by title): "PyTexas Meetup Attendance <DATE>" and "Questions for <SPEAKER>".

## Creating the Month Folder

1. Search Drive for the year folder (title equals the four-digit year). Its parent is the meetups root.
2. If the year folder does not exist yet (January), create it there first.
3. Create the month folder inside it, titled `YYYY-MM-DD` (the meetup date).

## Creating the Attendance and Questions Forms

Google Forms cannot be authored or edited through the Drive MCP, but a template can be copied and the copy can be renamed.

1. Search the "Meetup Forms Template" folder for "PyTexas Meetup Attendance <DATE>" and "Questions for <SPEAKER>".
2. Copy each into the month folder, setting the copy's title at copy time (the `copy_file` `title` field):
   - `PyTexas Virtual Meetup Attendance YYYY-MM-DD`
   - `Questions for <Speaker Name>`
3. Put each form's edit URL in the run of show. Renaming the copy fixes only the Drive file name; the form's on-screen title and description still hold the `<DATE>` / `<SPEAKER>` placeholders, and editing form content is a human task. List it under HUMAN REQUIRED TASKS in the run of show.

Two things that stay human tasks every time, because the MCP cannot do them:

- **Publishing.** The public responder link does not exist until the form is published from its Send dialog in the browser. The edit-ID `/d/<id>/viewform` URL returns 401 to the public and the published `/d/e/.../viewform` returns 404 until then. Only the edit link is knowable at setup time; the responder and `forms.gle` links get pasted in after publishing.
- **The response sheet.** It does not exist until someone opens the form's Responses tab and clicks Link to Sheets.

## Creating the Run of Show

Build the run of show as a native Google Doc by writing markdown and uploading it with conversion, never as HTML.
HTML upload breaks bullets and mangles formatting.
A `.docx` upload also converts natively, but it has to be inlined as base64, which is large and fragile; markdown is the format to use.
Markdown import converts cleanly: native headings, nested bullets, bold, autolinked URLs, and a real Google Docs table (a pipe table whose first row becomes a bold header).

1. Compose the doc content as markdown per `run-of-show.md`.
2. Create it in the month folder titled `Run of Show YYYY-MM-DD` with `create_file`, `contentMimeType: text/markdown`, conversion left on (do not set `disableConversionToGoogleType`).
3. Read the file back and confirm it converted: headings present, the table shows `:-:` separators, the `FILL_ME_IN` markers survived. To keep a literal `<DATE>` / `<SPEAKER>` in the body, write it as `&lt;DATE&gt;`; a raw `<...>` is dropped as an HTML tag on import.
4. There is no in-place body edit through the MCP. To correct a doc after creation, trash it and recreate from updated markdown (trashing works when the connector is on the PyTexas account).

Fill what is known at setup time (month, speaker, talk, bio, form edit links, the local meetups table, announcements).
Everything a human must still do goes in the HUMAN REQUIRED TASKS block at the top of the doc and as `FILL_ME_IN` markers inline; `run-of-show.md` carries the exact structure.
