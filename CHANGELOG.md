# Changelog

All notable user-facing and repository-protocol changes are recorded here.

## [Unreleased]

### Fixed

- **nvim / configuration comments**: Explain the non-default two-space StyLua policy beside the TOML settings and document that the default column width is intentionally inherited. Formatting behavior is unchanged.
- **Zed / configuration intent**: Restore JSONC comments with per-setting intent, default comparisons, extension conditions, conflicts, maintainer-preference labels, and official references. Remove repeated panel and theme-mode defaults; effective behavior remains the same while local defaults can evolve naturally.

- **Starship / configuration intent**: Restore official Pure-preset provenance, default comparisons, right-prompt constraints, compact Git-status trade-offs, and runtime identity/privacy comments. Remove the redundant default Git-state format and make Python display activate only for a virtual environment; users who relied on project-file Python version detection should keep Starship's default detectors.
- **nvim / configuration intent**: Restore official starter provenance, default comparisons, bootstrap effects, plugin-version intent, disabled runtime capabilities, and theme conflicts beside the Lua settings. Remove redundant lazy.nvim `defaults.lazy` and `defaults.version` values, the StyLua column-width default, and generated LazyVim NEWS state; the lock file remains the deliberate plugin reproducibility boundary, while existing users keep the same effective plugin-loading and formatting behavior and regain their own news cursor.
- **WezTerm / configuration intent**: Restore default comparisons, intent, platform conditions, conflicts, and official-documentation comments; remove an unsupported deprecated KDE blur option, describe the remaining branch as generic Linux behavior, and make the Windows 11 backdrop effective with its required opacity. Linux users lose only the invalid blur request, while Windows users should review the newly effective transparent system material.
- **Fish / configuration intent**: Restore intent, condition, dependency, conflict, privacy, maintainer-preference labels, and official-documentation comments throughout the reference; guard interactive integrations and theme state, use documented abbreviation syntax, and prevent file-owned paths from persisting as universal state. Rustup and Android integration comments now distinguish reusable guards from toolchain preferences. Existing consumers should review PATH precedence, project-managed JDK selection, optional application startup behavior, and custom key bindings before adopting the corrected behavior.

### Removed

- **Zed / provider-specific preferences**: Remove registry agent installations, selected Google agent models/options, and the Copilot edit-prediction provider from the general reference. Existing consumer configurations are not changed automatically; users who intentionally use these services may retain their own settings, while new consumers should choose integrations from their installed tools and account preferences rather than inherit the maintainer's providers.

### Added

- **Zed / module and preferences**: Add sanitized editor settings and a double-Shift file-finder keymap with Vim editing, Catppuccin/Monaspace presentation, panel layout, and diagnostics. Existing users should review every preference and verify extensions, font/theme availability, autosave behavior, and key conflicts before adopting it; no credentials, private endpoints, or local state are included.
- **Starship / module and preferences**: Add a sanitized two-sided prompt with compact Git state, command duration, and Python environment context. Existing users should review shell initialization, Unicode/font support, narrow-terminal behavior, and the intentionally collapsed Git status before adopting it.
- **nvim / module and preferences**: Add a sanitized LazyVim 8 reference with C/C++, Rust, and TOML extras, locked plugin revisions, and a transparent Catppuccin theme. Existing users should not replace another plugin manager wholesale and must approve first-start network/bootstrap effects and any optional language-tool installation.
- **WezTerm / module and preferences**: Add a sanitized cross-platform terminal reference with guarded window effects, Catppuccin styling, a Monaspace-first font fallback, and a hidden tab bar. Existing users should review visibility, navigation, font availability, compositor support, and platform-specific decoration effects before adopting it.

### Changed

- **Zed / navigation and safety preferences**: Add quit confirmation, close-on-repeated-panel-toggle behavior, smart-case search, editor sticky scroll, a six-line vertical navigation margin, and Markdown-only editor-width wrapping. Existing consumer configurations remain unchanged until approved; adopters should review scripted quit flows, panel shortcut expectations, reduced space in short panes, and visual wrapping before merging these settings.
- **Zed / reference filenames**: Rename the commented repository references to `settings.jsonc` and `keymap.jsonc` so hosting and editing tools recognize their JSONC syntax. Consumer AI must still merge them into Zed's required `settings.json` and `keymap.json` target files; existing user configurations do not need to be renamed.
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
