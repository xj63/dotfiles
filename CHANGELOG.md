# Changelog

All notable user-facing and repository-protocol changes are recorded here.

## [Unreleased]

### Added

- **repository**: Add a deterministic Configuration Audit for known secrets, private identifiers, personal paths, supported configuration syntax, and Local Consumer State boundaries.
- **repository**: Add a versioned commit hook and pull-request workflow that delegate to the same repository check interface.
- **repository / review protocol**: Add a provider-replaceable semantic Configuration Audit after deterministic CI. Pull requests now receive normalized Blocking and Advisory findings; maintainers must configure the documented provider credential before making the new check required. Existing consumer configurations require no migration.
