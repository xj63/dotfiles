# Starship

## Purpose and environment

This module is the maintainer's compact two-sided Starship prompt. It was validated with Starship 1.26.0 and Fish 4.9.2 on macOS 26.6.2. Starship is cross-shell and cross-platform, but right-prompt behavior and shell initialization differ by shell.

## Prerequisites and installation

Starship is required; detect it with `command -v starship` and inspect its version with `starship --version`. Use the official installation guide at https://starship.rs/guide/#step-1-install-starship only after the user approves. Read the official configuration and default-value reference at https://starship.rs/config/ before adapting a module. The prompt uses standard Unicode symbols and terminal colors but works best in a font that renders `❯`, `❮`, and `≡` clearly.

A supported shell must initialize Starship separately. The Fish module in this repository conditionally runs `starship init fish`; other shells should follow Starship's official shell-specific setup. Do not add a second initialization when the user's shell already loads Starship.

## Target configuration location

The reference `starship.toml` maps to `$STARSHIP_CONFIG` when that variable is set. Otherwise Starship reads `$XDG_CONFIG_HOME/starship.toml`, falling back to `~/.config/starship.toml`. Inspect the resolved path before proposing changes.

## Capabilities and maintainer preferences

The configuration is a documented derivative of Starship's official Pure preset, not a copy of the default prompt. The left prompt lists user, host, directory, and a modal success/error character. Username normally appears only for root, SSH, or a user unlike the login name, while hostname normally appears only over SSH; either can disclose runtime identity in recordings even though no identity is stored here. The right prompt shows Git branch, operation state, a deliberately compact aggregate status, command duration, and only the active Python virtual environment.

The two-sided layout, module order, colors, arrow characters, vi-mode indicator, dim Git branch/state, compact status encoding, and omission of many Starship defaults are Maintainer Preferences. The zero-width Git state markers intentionally collapse several file states into one `*` group and omit type-changed state; users who need per-state counts or symbols should retain their existing status format. `git_state.format` is omitted because the desired value is already Starship's default. Empty Python file/extension detectors are intentional non-default overrides that prevent project files alone from activating version detection.

## Known conflicts

Existing `format`, `right_format`, module blocks, shell prompt functions, or another prompt framework conflict directly. A narrow terminal can cause the right prompt to disappear or reflow; Bash requires Ble.sh 0.4 or newer for right-prompt support. The user/host modules still follow Starship's visibility rules, so their presence in `format` does not guarantee they render.

## Safe validation

Parse and resolve the candidate configuration without installing shell hooks or changing prompt state:

```sh
STARSHIP_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/starship.toml" starship print-config >/dev/null
```

Stop on a TOML or Starship diagnostic. Reloading the shell or evaluating `starship init` changes the interactive session and requires confirmation.
