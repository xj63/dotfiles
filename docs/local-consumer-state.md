# Private local fallback

Use ignored `.local/` state only when a User Intent Record cannot live in comments or a Markdown document inside the application's configuration directory, and only after the user agrees to keep that context in this clone.

For Fish, a concise `.local/fish/intent.md` may record:

- the resolved target location;
- the user's current configuration goal and the reasons for non-obvious choices;
- the last reviewed release or commit as the Review Cursor.

Record current state, not an operation log. Never put credentials, configuration contents, backup contents, or unrelated user information in `.local/`. The entire directory is ignored by Git and is outside deterministic checks, local semantic-review context, commits, and releases. Because it is clone-local, it does not travel to another clone unless the user deliberately moves a sanitized intent record.
