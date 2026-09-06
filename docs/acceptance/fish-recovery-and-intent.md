# Fish recovery and intent acceptance

Date: 2026-09-07

The maintainer's local AI exercised the Issue #5 protocol in isolated temporary directories. No real Fish configuration or ignored state from this clone was read.

## Version-controlled target and validation failure

- Created a temporary Git repository with a tracked `config.fish` containing an unrelated `EDITOR` setting.
- Recorded the clean `HEAD` checkpoint and exact file-scoped `git restore --source=<checkpoint> -- config.fish` recovery command before editing.
- Added an intentionally incomplete Fish block. `fish --no-config --no-execute config.fish` failed with exit status 127.
- Stopped after validation failure. The scenario then supplied restoration approval and ran the recorded command.
- The restored file's SHA-256 matched its pre-edit SHA-256.

## Unversioned target

- Created an unversioned `config.fish` and copied only that affected file to a sibling `.backup` path before editing.
- Added a valid quiet-greeting setting while preserving the unrelated `EDITOR` setting. Safe Fish validation returned exit status 0.
- Exercised the disclosed copy-back recovery command after scripted approval. The restored file's SHA-256 matched its pre-edit SHA-256.

## Intent locations and privacy boundary

- Wrote and reread a directory-local Markdown record containing a current goal, reason, and Review Cursor.
- Exercised the last-resort `.local/fish/intent.md` location in a temporary clone using only a target placeholder, goal, reason, and Review Cursor.
- `git status --short --untracked-files=all` remained empty and `scripts/check all` passed without reading ignored state.
- The automated review-context tests additionally prove that ignored intent, ignored backups, external Consumer Configurations, and the target of a tracked README symlink do not enter local semantic-review input.
