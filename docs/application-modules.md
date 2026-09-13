# Authoring an Application Module

Create the module directly under the repository root using the application's name. Arrange its Reference Configuration relative to the application's native configuration root, then state the real user target location in `README.md`. A repository reference may use a syntax-explicit suffix such as `.jsonc` when that improves rendering; if the application requires another filename, document the exact rename or merge target. Do not add an `apps/` wrapper or a machine-readable manifest.

Write one coherent, sanitized Reference Configuration. When importing an existing configuration, preserve useful comments by default. Remove or rewrite a comment only when it exposes private information, is inaccurate for the supported version, merely narrates syntax, or describes a setting that no longer exists.

Before retaining an assignment, compare it with the official defaults for the module's tested application version. Omit a value that only repeats the upstream default. Keep an explicit default only when deliberately freezing behavior against a future upstream change, and state that stability intent beside it. Record the official source or configuration page used for non-obvious behavior; defaults are version-sensitive and must be rechecked when the tested version changes.

Explain irreducibly exclusive choices close to the setting and add alternative files only when comments cannot express a working choice. Formats that support comments should explain each capability group's goal, observable effect, applicability or dependency, important conflict, and whether it is a Reusable Rule or Maintainer Preference. Comments explain why the configuration exists, not just what its syntax says. Fish, Lua, TOML, and application-defined JSONC support inline comments. Strict JSON files such as generated lock state remain comment-free; put their corresponding explanation in the module README.

The README is ordinary English prose for people and AI tools. Include only subjects that apply: purpose, environment, prerequisites and official installation source, official configuration reference, target location, capabilities, preferences, conflicts, default-versus-override decisions, and safe validation. Purpose and environment can be a sentence rather than a fixed heading; the checker does not require a table, manifest, or empty section. Every runnable configuration still needs a portable target path, prerequisite statement, official configuration documentation, and safe validation guidance so an AI can place, interpret, and check it safely.

Make every non-core dependency traceable. When a setting or capability relies on a font, theme, icon pack, extension, plugin, language server, command, application, or platform service, name the exact dependency, identify the setting or capability that uses it, explain how to detect whether it is available, and link to its first-party installation or project source. State whether the dependency is required for startup, required only when the capability is selected or invoked, automatically acquired by the application's own manager, or merely improves rendering. Never install one solely because it appears in a Reference Configuration; installation remains a separately confirmed action.

`scripts/check all` enforces the structural presence of official configuration guidance and supported syntax. The local semantic Configuration Audit remains responsible for judging whether the cited source is authoritative, comments are useful, and explicit values are genuine overrides rather than undocumented copies of defaults.

English `README.md` is normative. A translation is an optional entry point named like `README.zh-CN.md`; it links to `README.md` and says the English README is normative. Keep configuration truth and normative rules in the English source so translations cannot silently become a second contract.

For every user-affecting module edit, add a categorized `[Unreleased]` line in the same change:

```text
- **Application / category**: Describe the change and user impact. Explain migration when relevant.
```

Run `scripts/check all`. Its module diagnostics describe missing information by policy rule rather than requiring exact headings or prose.
