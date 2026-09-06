# Changelog

All notable user-facing and repository-protocol changes are recorded here.

## [Unreleased]

### Added

- **repository**: Add a deterministic Configuration Audit for known secrets, private identifiers, personal paths, supported configuration syntax, and Local Consumer State boundaries.
- **repository**: Add a versioned commit hook and pull-request workflow that delegate to the same repository check interface.
- **repository / review protocol**: Define a local AI Configuration Audit for tracked pull-request changes, with Blocking and Advisory findings recorded in the pull request. GitHub CI remains deterministic and no repository AI credential is required. Existing consumer configurations require no migration.
- **Fish / module and guidance**: Add the first runnable Fish Reference Configuration, a human entry point with a copyable AI prompt, and the eight-stage Consumer AI workflow. Users should adapt selected capabilities into their existing Fish configuration and record intent locally; no existing Consumer Configuration changes automatically.
- **Fish / recovery and intent**: Define exact Git and file-backup Recovery Paths plus the approved ignored `.local/` fallback for Fish intent. Existing users need no migration; an AI should select the first viable intent location and never place configuration copies or credentials in clone-local state.
- **repository / review protocol**: Add a bounded local review-context command that emits only the tracked pull-request diff, Review Policy, and affected module guidance after deterministic checks pass. Local AI audits should use this command; no hosted AI service or credential is introduced.
