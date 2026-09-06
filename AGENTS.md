# Agent guidance

## Agent skills

### Issue tracker

Issues and specs are tracked in GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the repository's canonical triage labels. See `docs/agents/triage-labels.md`.

### Domain docs

This repository uses a single-context domain-documentation layout. See `docs/agents/domain.md`.

### Architecture

When changing the repository layout, application modules, consumer-AI workflow, review gates, or release process, read `docs/architecture.md` and the relevant ADRs under `docs/adr/` first.

### Review policy

Before committing repository changes or auditing configuration safety, read `REVIEW.md`. Install the versioned commit hook with `scripts/install-hooks`; use `scripts/check all` for a full deterministic check.

When asked to **audit the current repository using the Review Policy**, run `scripts/check all` first. If it passes, use the current local AI session to inspect tracked repository content under `REVIEW.md`; do not call a remote AI provider. Report Blocking and Advisory Findings separately. Never read `.local/`, backups, Consumer Configurations, credentials, or unrelated filesystem content for semantic review.

Before creating or updating a pull request, perform the same local semantic review over `git diff origin/main...HEAD`, this policy, and only the README files of affected Application Modules. Put the audit summary in the pull-request description or a review comment.
