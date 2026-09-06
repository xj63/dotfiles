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
- **Fish / update protocol**: Add Review Cursor-based, Fish-filtered change assessment and a read-only context command. Existing Consumer Configurations do not change automatically; their AI should present an impact report, obtain confirmation for behavior, dependency, or preference changes, and advance the cursor only after accepted changes validate.
- **repository / consumer protocol**: Define application-scoped update assessment, ancestry checks, module-removal handling, and required shared-protocol change information. Existing users need no migration; their AI should use the selected module's update guidance and stop on missing or divergent history.
- **repository / consumer protocol**: Make the natural-language Application Module contract discoverable and deterministically check target, prerequisite, validation, translation-source, privacy, syntax, and change-information obligations. Existing Fish users need no migration; future modules follow the same root-level, comment-first contract without a manifest.
