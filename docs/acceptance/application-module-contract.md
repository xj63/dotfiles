# Application Module contract acceptance

Date: 2026-09-07

The deterministic checker was exercised against temporary Git repositories; no production module was added.

- A root-level `nova/` module passed with one commented TOML Reference Configuration and a short prose README. Discovery used the root README path and contained no Fish name, manifest, table, or fixed section sequence.
- The Nova README stated its portable native-root target, required application version, optional preference, and safe validation in ordinary sentences.
- Focused fixtures omitted target location, prerequisites, or validation and received the corresponding `module.*-guidance` diagnostic naming `nova/README.md`.
- A private home path in the temporary module was rejected by the shared privacy rule, and invalid JSON remains covered by the shared syntax rule.
- A Chinese entry point without a link and normative-English statement was rejected as a drifting second source of truth.
- Staged and committed module edits without a categorized `[Unreleased]` entry were rejected; a categorized Nova entry passed. Removing an entire module was also treated as a user-affecting edit.
- Formats with comments keep capability conditions and Maintainer Preferences beside the native setting. The authoring guide directs commentless formats to keep those explanations in README prose and keeps alternatives exceptional.
