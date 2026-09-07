# Changelog

All notable user-facing and repository-protocol changes are recorded here.

## [Unreleased]

### Fixed

- **nvim / configuration comments**: Explain the non-default two-space StyLua policy beside the TOML settings and document that the default column width is intentionally inherited. Formatting behavior is unchanged.
- **Zed / configuration intent**: Restore JSONC comments with per-setting intent, default comparisons, extension/provider conditions, data-sharing implications, conflicts, maintainer-preference labels, and official references. Remove repeated panel, agent, thinking, edit-display, and theme-mode defaults; effective behavior remains the same while local defaults can evolve naturally.
- **Starship / configuration intent**: Restore official Pure-preset provenance, default comparisons, right-prompt constraints, compact Git-status trade-offs, and runtime identity/privacy comments. Remove the redundant default Git-state format and make Python display activate only for a virtual environment; users who relied on project-file Python version detection should keep Starship's default detectors.
- **nvim / configuration intent**: Restore official starter provenance, default comparisons, bootstrap effects, plugin-version intent, disabled runtime capabilities, and theme conflicts beside the Lua settings. Remove redundant lazy.nvim and StyLua defaults plus generated LazyVim NEWS state; existing users keep the same effective plugin-loading and formatting behavior but regain their own news cursor.
- **WezTerm / configuration intent**: Restore default comparisons, intent, platform conditions, conflicts, and official-documentation comments; remove an unsupported deprecated KDE blur option and make the Windows 11 backdrop effective with its required opacity. Linux users lose only the invalid blur request, while Windows users should review the newly effective transparent system material.
- **Fish / configuration intent**: Restore intent, condition, dependency, conflict, privacy, maintainer-preference labels, and official-documentation comments throughout the reference; guard interactive integrations and theme state, use documented abbreviation syntax, and prevent file-owned paths from persisting as universal state. Rustup and Android integration comments now distinguish reusable guards from toolchain preferences. Existing consumers should review PATH precedence, project-managed JDK selection, optional application startup behavior, and custom key bindings before adopting the corrected behavior.

### Added

- **Zed / module and preferences**: Add sanitized editor settings and a double-Shift file-finder keymap with Vim editing, Catppuccin/Monaspace presentation, panel layout, diagnostics, optional agent servers, and edit predictions. Existing users should review every preference and verify extensions, provider accounts, models, font/theme availability, autosave behavior, and key conflicts before adopting it; no conversations, credentials, private endpoints, or local agent instructions are included.
- **Starship / module and preferences**: Add a sanitized two-sided prompt with compact Git state, command duration, and Python environment context. Existing users should review shell initialization, Unicode/font support, narrow-terminal behavior, and the intentionally collapsed Git status before adopting it.
- **nvim / module and preferences**: Add a sanitized LazyVim 8 reference with C/C++, Rust, and TOML extras, locked plugin revisions, and a transparent Catppuccin theme. Existing users should not replace another plugin manager wholesale and must approve first-start network/bootstrap effects and any optional language-tool installation.
- **WezTerm / module and preferences**: Add a sanitized cross-platform terminal reference with guarded window effects, Catppuccin styling, a Monaspace-first font fallback, and a hidden tab bar. Existing users should review visibility, navigation, font availability, compositor support, and platform-specific decoration effects before adopting it.

### Changed

- **repository / module authoring protocol**: Require official configuration references, preserve useful source comments, distinguish intent from syntax narration, and omit repeated upstream defaults unless a stability reason is documented. Existing modules have been reassessed against their tested application versions; future module authors receive a deterministic missing-guidance diagnostic and local semantic review handles source quality and default equivalence.
- **repository / consumer protocol**: List every available Application Module in the human entry point so users and AI can select Fish, WezTerm, Neovim, Starship, or Zed without inspecting unrelated modules. Existing consumer configurations do not change.
- **nvim / module guidance**: Remove empty user-extension placeholders and place update-checker and runtime-plugin preference explanations beside their settings. Existing runtime behavior does not change because the removed files contained no code.
- **WezTerm / module guidance**: Explain the Linux/KDE blur and Windows backdrop conditions beside their settings. Existing WezTerm behavior does not change.
- **Starship / module guidance**: Correctly label compact zero-width Git status markers as a Maintainer Preference rather than a reusable rule. Existing prompt behavior does not change.
- **Zed / module guidance**: Remove inert empty proxy and context-server placeholders, then explain CLI window and Git tree behavior. Existing users with a proxy or context server should preserve their local value; other documented behavior is unchanged.
- **Fish / capability guidance**: Explain when `noproxy` is useful and that it can break proxy-dependent network access. Existing Fish behavior does not change until the function is invoked.
- **Fish / validation guidance**: Extend safe validation and inspection guidance to cover `config.fish`, `conf.d`, functions, and all optional tools. Existing Fish behavior does not change.
- **Fish / behavior and preferences**: Expand the reference into the maintainer's sanitized daily setup with vi bindings, theme colors, guarded toolchain integrations, and command helpers. Existing consumers should review each optional dependency and name conflict before adopting anything; the former quiet greeting changes to an explicit dynamic greeting only when selected.

## [1.0.0] - 2026-09-07

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
- **repository / consumer protocol**: Publish the repeatable Semantic Version release procedure and the first stable Review Cursor. Existing Consumer Configurations do not change; fresh users may record `v1.0.0`, while existing users assess it from their earlier cursor before any edits.
