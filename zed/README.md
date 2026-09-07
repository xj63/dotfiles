# Zed

## Purpose and environment

This module is the maintainer's macOS-oriented Zed editor setup. It was validated with Zed 1.18.1 on macOS 26.6.2. It combines Vim-style editing, right-docked project tools, a left-docked agent panel, Catppuccin themes, Monaspace, inline assistance, and a double-Shift file finder.

## Prerequisites and installation

Zed is required; on macOS detect it with `command -v zed` or inspect `/Applications/Zed.app`, then run `zed --version`. Obtain it from the official download page at https://zed.dev/download only after the user approves.

The Catppuccin icon/theme variants, Monaspace Neon Frozen font, Gemini agent server, Codex ACP server, Google models, GitHub Copilot edit predictions, and `cargo-tom` LSP configuration are optional external capabilities. Detect their availability in the user's Zed installation and account before selecting them. Never copy credentials, provider endpoints, conversations, prompt databases, or extension state into this module, and never sign in or install an extension without confirmation.

## Target configuration location

The reference files map to `$XDG_CONFIG_HOME/zed/settings.json` and `$XDG_CONFIG_HOME/zed/keymap.json`, falling back to `~/.config/zed/` when `XDG_CONFIG_HOME` is unset. Merge selected settings into existing files and preserve unrelated language, task, extension, collaboration, and remote-development configuration.

## Capabilities and maintainer preferences

CLI requests open a new window. The workspace panels dock on the right, the Git panel uses its tree view, and the agent docks on the left. The editor follows the system light/dark mode with Catppuccin Blur themes, uses Monaspace, enables Vim mode, wrapped relative line numbers, focus-change autosave, automatic minimap visibility, inlay hints, inline diagnostics, signature help, and edit predictions. Objective-C extensions are associated with C++, telemetry diagnostics and metrics are disabled, and double Shift opens the file finder.

All of these are Maintainer Preferences. Agent provider/model names are examples of the maintainer's current selection, not universal recommendations and not promises that a model remains available. In particular, `reasoning_effort = high`, the default write profile, modifier-to-send, telemetry choices, focus-change autosave, panel placement, and `shift shift` binding can materially change behavior.

## Known conflicts

Existing CLI open behavior, panel docks or Git panel presentation, themes, icon themes, font selection, Vim mode, line numbers, autosave policy, minimap, hints, diagnostics, signature help, file associations, LSP initialization, telemetry, agent providers/models, edit-prediction provider, or double-Shift binding conflict directly. A missing theme, font, extension, server, provider account, or model may cause Zed to reject or ignore only that setting. Preserve locally configured proxy settings, credentials, and endpoints outside the reference.

## Safe validation

Validate the strict JSON syntax without opening Zed or loading provider state:

```sh
python3 -m json.tool "${XDG_CONFIG_HOME:-$HOME/.config}/zed/settings.json" >/dev/null
python3 -m json.tool "${XDG_CONFIG_HOME:-$HOME/.config}/zed/keymap.json" >/dev/null
```

JSON syntax validation cannot prove that installed Zed supports every setting or model. After it passes, inspect Zed's settings diagnostics. Reloading Zed, signing in, installing extensions, or exercising agent and edit-prediction providers can change application or account state and requires confirmation.
