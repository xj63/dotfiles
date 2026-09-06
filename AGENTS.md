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
