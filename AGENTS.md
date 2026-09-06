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

When adding or changing an Application Module, also read `docs/application-modules.md`. Complete the module when its native-root file layout, natural-language guidance, inline capability explanations, safe validation, and categorized `[Unreleased]` entry all pass `scripts/check all`.

## Consumer configuration guidance

When a user asks for help applying a module to their own configuration, complete these stages in order:

1. **Understand the goal** and identify unresolved choices.
2. **Inspect the existing configuration and environment**, including application and system versions, target paths, dependencies, and conflicts.
3. **Read the relevant Application Module** and only the repository guidance it references. For Fish, start with `fish/README.md`.
4. **Present a plan and impact** covering the smallest proposed edits, behavior changes, prerequisites, conflicts, recovery, and validation. Do not modify yet.
5. **Obtain confirmation** before behavior changes, overwrites, dependency installation, application restarts, or other consequential actions.
6. **Establish a Recovery Path and modify** only the accepted scope, preserving unrelated settings. Prefer the user's version control; otherwise follow the module's recovery guidance.
7. **Validate** with the module's safe, read-only or side-effect-free checks. Stop on failure and offer restoration before any further action.
8. **Preserve user intent and the Review Cursor** beside the Consumer Configuration when possible. Record current goals and reasons, not an operation log; never store credentials.

Consumer Configurations remain independent from this repository. Never synchronize them automatically or inspect unrelated Application Modules. If intent cannot live in configuration comments or a Markdown file inside a directory-based configuration, ask before using ignored `.local/` state in the clone.

### Upstream update assessment

When a user asks about newer repository changes, read the Review Cursor from their intent record and the update instructions in the selected module. Generate the application-scoped change context, then compare each relevant upstream intent and diff with the current Consumer Configuration. Stop if the cursor is not an ancestor of the target; resolve the expected history instead of treating a rollback or divergent branch as an update. The impact report is complete when every relevant change, including module removal and shared consumer-protocol changes, is classified as already satisfied, applicable, conflicting, or irrelevant to the user's goal.

Present a focused impact report before proposing edits. A pull or a reviewed upstream change never authorizes configuration modification. Obtain confirmation for every behavior, dependency, or Maintainer Preference change. If the user declines the update, leave the Consumer Configuration and Review Cursor unchanged. If the user accepts a subset, establish recovery, apply only the accepted changes, validate, update current intent, and advance the Review Cursor to the reviewed upstream state.

### Review policy

Before committing repository changes or auditing configuration safety, read `REVIEW.md`. Install the versioned commit hook with `scripts/install-hooks`; use `scripts/check all` for a full deterministic check.

When asked to **audit the current repository using the Review Policy**, run `scripts/check all` first. If it passes, use the current local AI session to inspect tracked repository content under `REVIEW.md`; do not call a remote AI provider. Report Blocking and Advisory Findings separately. Never read `.local/`, backups, Consumer Configurations, credentials, or unrelated filesystem content for semantic review.

Before creating or updating a pull request, run `scripts/review-context origin/main` and use only its output for the local semantic review. Put the audit summary in the pull-request description or a review comment.
