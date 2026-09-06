# Changelog

All notable user-facing and repository-protocol changes are recorded here.

## [Unreleased]

### Added

- **repository**: Add a deterministic Configuration Audit for known secrets, private identifiers, personal paths, supported configuration syntax, and Local Consumer State boundaries.
- **repository**: Add a versioned commit hook and pull-request workflow that delegate to the same repository check interface.
- **repository / review protocol**: Define a local AI Configuration Audit for tracked pull-request changes, with Blocking and Advisory findings recorded in the pull request. GitHub CI remains deterministic and no repository AI credential is required. Existing consumer configurations require no migration.
