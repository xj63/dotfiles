# Starship

## Purpose and environment

This module is the maintainer's compact two-sided Starship prompt. It was validated with Starship 1.26.0 and Fish 4.9.2 on macOS 26.6.2. Starship is cross-shell and cross-platform, but right-prompt behavior and shell initialization differ by shell.

## Prerequisites and installation

Starship is required; detect it with `command -v starship` and inspect its version with `starship --version`. Use the official installation guide at https://starship.rs/guide/#step-1-install-starship only after the user approves. The prompt uses standard Unicode symbols and terminal colors but works best in a font that renders `❯`, `❮`, and `≡` clearly.

A supported shell must initialize Starship separately. The Fish module in this repository conditionally runs `starship init fish`; other shells should follow Starship's official shell-specific setup. Do not add a second initialization when the user's shell already loads Starship.

## Target configuration location

The reference `starship.toml` maps to `$STARSHIP_CONFIG` when that variable is set. Otherwise Starship reads `$XDG_CONFIG_HOME/starship.toml`, falling back to `~/.config/starship.toml`. Inspect the resolved path before proposing changes.

## Capabilities and maintainer preferences

The left prompt shows user, host, directory, and a modal success/error character. The right prompt shows Git branch, operation state, a deliberately compact aggregate status, command duration, and the active Python virtual environment.

The two-sided layout, module order, colors, arrow characters, vi-mode indicator, dim Git branch, compact status encoding, and omission of many Starship defaults are Maintainer Preferences. The zero-width Git state markers intentionally collapse several file states into one `*` group; users who need per-state counts or symbols should retain their existing status format.

## Known conflicts

Existing `format`, `right_format`, module blocks, shell prompt functions, or another prompt framework conflict directly. A narrow terminal can cause the right prompt to disappear or reflow. The user/host modules still follow Starship's own visibility rules, so their presence in `format` does not guarantee they always render.

## Safe validation

Parse and resolve the candidate configuration without installing shell hooks or changing prompt state:

```sh
STARSHIP_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/starship.toml" starship print-config >/dev/null
```

Stop on a TOML or Starship diagnostic. Reloading the shell or evaluating `starship init` changes the interactive session and requires confirmation.
