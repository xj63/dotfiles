# Issue tracker: GitHub

Issues and specs for this repo live as GitHub issues. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --comments`, filtering comments by `jq` and also fetching labels.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Comment on an issue**: `gh issue comment <number> --body "..."`.
- **Apply or remove labels**: `gh issue edit <number> --add-label "..."` or `--remove-label "..."`.
- **Close**: `gh issue close <number> --comment "..."`.

Infer the repository from `git remote -v`; `gh` does this automatically inside this clone.

## Pull requests as a triage surface

**PRs as a request surface: no.** Set this to `yes` if external pull requests should enter the same triage flow as issues.

When enabled, use the equivalent `gh pr` operations. GitHub shares one number space across issues and pull requests, so resolve an ambiguous `#42` with `gh pr view 42` and fall back to `gh issue view 42`.

## Skill operations

- When a skill says **publish to the issue tracker**, create a GitHub issue.
- When a skill says **fetch the relevant ticket**, run `gh issue view <number> --comments`.

## Wayfinding operations

- The map is one issue labelled `wayfinder:map`.
- Decision tickets are linked as GitHub sub-issues where available, with a task-list fallback.
- Represent blocking relationships with native GitHub issue dependencies where available; otherwise use a `Blocked by: #<n>` line.
- A ticket is available only when it is open, unassigned, and has no open blockers.
- Claim work by assigning the issue to the current user; resolve it with a concluding comment and close it.
