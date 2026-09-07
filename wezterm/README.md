# WezTerm

## Purpose and environment

This module is the maintainer's compact, cross-platform WezTerm appearance configuration. It was validated with WezTerm `20240203-110809-5046fc22` on macOS 26.6.2. Platform branches cover macOS, Linux/KDE, and Windows, but the visual result depends on the compositor and installed fonts.

## Prerequisites and installation

WezTerm is required; detect it with `command -v wezterm` and inspect its version with `wezterm --version`. Install it from the official project at https://wezterm.org/installation.html only after the user approves. `Monaspace Neon Frozen` is an optional font preference; the configuration falls back to `Menlo` when it is unavailable. Catppuccin Mocha is a color scheme bundled with the tested WezTerm release.

## Target configuration location

Place or merge `wezterm.lua` at `$XDG_CONFIG_HOME/wezterm/wezterm.lua`, falling back to `~/.config/wezterm/wezterm.lua` when `XDG_CONFIG_HOME` is unset. WezTerm also supports `~/.wezterm.lua`; inspect which convention the user already follows and do not create a second competing file.

## Capabilities and maintainer preferences

The reusable part detects WezTerm's target triple before applying platform-specific window settings. Everything visible is a Maintainer Preference: Catppuccin Mocha, a 14-point Monaspace-first font stack, a hidden tab bar, macOS resize-only decorations with 80% opacity and strong blur, lighter Linux transparency with KDE blur, and the Windows tabbed system backdrop.

Disabling the tab bar hides tab navigation and status information. Transparency and blur can reduce contrast or performance, and KDE blur requires compositor support. `window_decorations = "RESIZE"` removes the normal macOS title bar controls. Present these consequences separately before adopting them.

## Known conflicts

Existing color, font, tab, window-decoration, opacity, blur, or backdrop settings conflict directly. A user who relies on tabs should keep the tab bar or add an alternative navigation surface. Preserve custom key mappings, domains, launch menus, environment variables, and SSH settings that are outside this reference.

## Safe validation

Run the following read-only command against the candidate file. It loads the configuration and prints resolved key assignments without starting a terminal window:

```sh
wezterm --config-file "${XDG_CONFIG_HOME:-$HOME/.config}/wezterm/wezterm.lua" show-keys --lua >/dev/null
```

Stop on any Lua or configuration diagnostic. Opening or reloading WezTerm changes the visible application state and requires confirmation.
