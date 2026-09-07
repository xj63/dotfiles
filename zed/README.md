# Zed

## Purpose and environment

This module is the maintainer's macOS-oriented Zed editor setup. It was validated with Zed 1.18.1 on macOS 26.6.2. It combines Vim-style editing, safer application exit, efficient panel and search navigation, a tree-style Git panel, Catppuccin themes, Monaspace, visible code intelligence, Markdown wrapping, and a double-Shift file finder.

## Prerequisites and installation

Zed is required; on macOS detect it with `command -v zed` or inspect `/Applications/Zed.app`, then run `zed --version`. Obtain it from the official download page at https://zed.dev/download only after the user approves. Read the official configuration guide at https://zed.dev/docs/configuring-zed and compare inherited values with the versioned defaults before adding an override.

The Catppuccin icon/theme variants, Monaspace Neon Frozen font, and `cargo-tom` LSP configuration are optional external capabilities. Detect their availability in the user's Zed installation before selecting them. Never copy extension state into this module, and never install an extension without confirmation.

## Target configuration location

The repository uses `settings.jsonc` and `keymap.jsonc` so GitHub and other tools recognize the commented syntax. They are reference filenames, not Zed's native filenames. When adapting them, merge the selected content into `$XDG_CONFIG_HOME/zed/settings.json` and `$XDG_CONFIG_HOME/zed/keymap.json`, falling back to `~/.config/zed/` when `XDG_CONFIG_HOME` is unset. Do not place competing `.jsonc` files in the user's Zed configuration directory, and preserve unrelated language, task, extension, collaboration, and remote-development configuration.

## Capabilities and maintainer preferences

CLI requests open a new window, quitting requires confirmation, a repeated focused-panel shortcut closes the panel, smart-case search follows uppercase queries, editor sticky scroll keeps the current scope visible, and keyboard navigation preserves six surrounding lines. The Git panel uses its non-default tree view, while Zed's default panel docks are inherited rather than repeated. The editor follows the default system mode with explicit Catppuccin Blur themes, uses Monaspace, enables Vim mode, wrapped relative line numbers, focus-change autosave, automatic minimap visibility, inlay hints, inline diagnostics, and signature help. Markdown wraps visually at the editor width without changing code wrapping or inserting line breaks. Objective-C extensions are associated with C++, telemetry diagnostics and metrics are disabled, and double Shift opens the file finder.

All explicit values are Maintainer Preferences. Provider-specific agent, model, and edit-prediction selections are deliberately absent because they depend on user accounts, installed integrations, availability, and personal workflow. The default system theme mode and panel docks are omitted because they add no behavior. In particular, quit confirmation, panel toggle semantics, sticky headers, a larger scroll margin, Markdown wrapping, telemetry choices, focus-change autosave, and `shift shift` can materially change behavior.

## Known conflicts

Existing CLI open behavior, quit handling, panel shortcut expectations, search case rules, sticky scroll, scroll margins, Markdown language settings, Git panel presentation, themes, icon themes, font selection, Vim mode, line numbers, autosave policy, minimap, hints, diagnostics, signature help, file associations, LSP initialization, telemetry, or double-Shift binding conflict directly. Quit confirmation can interrupt automated exits; sticky headers and a six-line margin reduce usable height in short panes; Markdown visual wrapping can obscure long source lines. Focus-change autosave can run formatters or other save hooks. A missing theme, font, extension, or language server may cause Zed to reject or ignore only that setting. Preserve locally configured integrations, credentials, and endpoints outside the reference.

## Safe validation

Zed officially parses its `.json` configuration files as JSONC, including comments and trailing commas. The `.jsonc` suffix is used only for these repository references. From this knowledge-base clone, validate them without opening Zed or loading provider state:

```sh
scripts/check all
```

The repository check validates JSONC syntax but cannot prove that a consumer's installed Zed supports every setting. For a consumer configuration, use Zed's Settings Editor/schema diagnostics and keymap editor; `dev: open key context view` diagnoses binding context. Reloading Zed or installing extensions changes application state and requires confirmation.
