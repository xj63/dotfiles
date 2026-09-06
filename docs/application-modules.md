# Authoring an Application Module

Create the module directly under the repository root using the application's name. Arrange its Reference Configuration relative to the application's native configuration root, then state the real user target location in `README.md`. Do not add an `apps/` wrapper or a machine-readable manifest.

Write one coherent, sanitized Reference Configuration. Explain irreducibly exclusive choices close to the setting and add alternative files only when comments cannot express a working choice. Formats that support comments should explain each capability's goal, condition, conflict, and subjective Maintainer Preference beside the setting. For formats such as JSON that cannot safely carry comments, put the corresponding explanation in the module README.

The README is ordinary English prose for people and AI tools. Include only subjects that apply: purpose, environment, prerequisites and official installation source, target location, capabilities, preferences, conflicts, and safe validation. Purpose and environment can be a sentence rather than a fixed heading; the checker does not require a table, manifest, or empty section. Every runnable configuration still needs a portable target path, prerequisite statement, and safe validation guidance so an AI can place and check it safely.

English `README.md` is normative. A translation is an optional entry point named like `README.zh-CN.md`; it links to `README.md` and says the English README is normative. Keep configuration truth and normative rules in the English source so translations cannot silently become a second contract.

For every user-affecting module edit, add a categorized `[Unreleased]` line in the same change:

```text
- **Application / category**: Describe the change and user impact. Explain migration when relevant.
```

Run `scripts/check all`. Its module diagnostics describe missing information by policy rule rather than requiring exact headings or prose.
