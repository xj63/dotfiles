# Zed

## Purpose and environment

This module is the maintainer's macOS-oriented Zed editor setup. It was validated with Zed 1.18.1 on macOS 26.6.2. It combines Vim-style editing, right-docked project tools, a left-docked agent panel, Catppuccin themes, Monaspace, inline assistance, and a double-Shift file finder.

## Prerequisites and installation

Zed is required; on macOS detect it with `command -v zed` or inspect `/Applications/Zed.app`, then run `zed --version`. Obtain it from the official download page at https://zed.dev/download only after the user approves. Read the official configuration guide at https://zed.dev/docs/configuring-zed and compare inherited values with the versioned defaults before adding an override.

The Catppuccin icon/theme variants, Monaspace Neon Frozen font, Gemini agent server, Codex ACP server, Google models, GitHub Copilot edit predictions, and `cargo-tom` LSP configuration are optional external capabilities. Detect their availability in the user's Zed installation and account before selecting them. Never copy credentials, provider endpoints, conversations, prompt databases, or extension state into this module, and never sign in or install an extension without confirmation.

## Target configuration location

The reference files map to `$XDG_CONFIG_HOME/zed/settings.json` and `$XDG_CONFIG_HOME/zed/keymap.json`, falling back to `~/.config/zed/` when `XDG_CONFIG_HOME` is unset. Merge selected settings into existing files and preserve unrelated language, task, extension, collaboration, and remote-development configuration.

## Capabilities and maintainer preferences

CLI requests open a new window, and the Git panel uses its non-default tree view. Zed's default right-side panel docks and left agent dock are inherited rather than repeated. The editor follows the default system mode with explicit Catppuccin Blur themes, uses Monaspace, enables Vim mode, wrapped relative line numbers, focus-change autosave, automatic minimap visibility, inlay hints, inline diagnostics, signature help, and Copilot edit predictions. Objective-C extensions are associated with C++, telemetry diagnostics and metrics are disabled, and double Shift opens the file finder.

All explicit values are Maintainer Preferences. Agent provider/model names are examples of the maintainer's current selection, not universal recommendations and not promises that a model remains available. The default write profile, disabled thinking, automatic prediction display, system theme mode, and default panel docks are omitted because they add no behavior. In particular, `reasoning_effort = high`, modifier-to-send, telemetry choices, focus-change autosave, provider selection, and `shift shift` can materially change behavior.

## Known conflicts

Existing CLI open behavior, Git panel presentation, themes, icon themes, font selection, Vim mode, line numbers, autosave policy, minimap, hints, diagnostics, signature help, file associations, LSP initialization, telemetry, agent providers/models, edit-prediction provider, or double-Shift binding conflict directly. Focus-change autosave can run formatters or other save hooks. Copilot and external agents may transmit editing context and require authentication. A missing theme, font, extension, server, provider account, or model may cause Zed to reject or ignore only that setting. Preserve locally configured proxy settings, credentials, and endpoints outside the reference.

## Safe validation

Zed officially parses these files as JSONC, including comments and trailing commas. From this knowledge-base clone, validate the tracked reference without opening Zed or loading provider state:

```sh
scripts/check all
```

The repository check validates JSONC syntax but cannot prove that a consumer's installed Zed supports every setting or model. For a consumer configuration, use Zed's Settings Editor/schema diagnostics and keymap editor; `dev: open key context view` diagnoses binding context. Reloading Zed, signing in, installing extensions, or exercising agent and edit-prediction providers can change application or account state and requires confirmation.
