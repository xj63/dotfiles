# AeroSpace

## Purpose and environment

This module is a compact, keyboard-driven AeroSpace setup for macOS 13 or newer on Apple Silicon or Intel. It was curated against AeroSpace 0.21.3-Beta and its `config-version = 2` behavior. The maintainer's installed 0.19.2-Beta configuration was used only as source material; users of older releases should upgrade or adapt against their version's documentation instead of assuming compatibility.

## Prerequisites and installation

AeroSpace 0.21.3-Beta or a compatible newer release is required. Detect the application version with `/Applications/AeroSpace.app/Contents/MacOS/AeroSpace --version`; if the optional CLI is on `PATH`, `aerospace --version` is equivalent. AeroSpace also requires macOS Accessibility permission to manage windows.

Use the official [installation instructions](https://nikitabobko.github.io/AeroSpace/guide#installation). The documented Homebrew route is `brew install --cask nikitabobko/tap/aerospace`, and the official GitHub releases provide a manual download. Explain a missing or older installation and obtain explicit approval before installing or upgrading it.

The Reference Configuration uses only commands built into AeroSpace and the macOS Accessibility service. Verify permission under System Settings > Privacy & Security > Accessibility; Apple's [Accessibility permission guidance](https://support.apple.com/guide/mac-help/mchld5a35146/mac) is the platform source, and changing access requires confirmation. The reference has no font, theme, plugin, shell-command, or third-party application dependency. Application launchers and routing rules that would introduce such dependencies are deliberately excluded.

Read the official [configuration guide](https://nikitabobko.github.io/AeroSpace/guide#configuring-aerospace), [default configuration](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/config-examples/default-config.toml), and [command reference](https://nikitabobko.github.io/AeroSpace/commands) before adapting this reference.

## Target configuration location

The repository's `aerospace.toml` maps to `${XDG_CONFIG_HOME}/aerospace/aerospace.toml`, with `XDG_CONFIG_HOME` falling back to `~/.config`. AeroSpace also accepts the older `~/.aerospace.toml` location and reports an ambiguity if both files exist. Inspect which path is already active with `aerospace config --config-path`; merge accepted settings into that one file and never create the second path alongside it.

## Included capabilities and preferences

The reference starts AeroSpace at login, opens workspace 1 after startup, disables native application hiding, moves the pointer lazily with keyboard focus, and defines a single Vim-oriented main binding mode. It supports directional focus and movement, smart resizing, floating and fullscreen toggles, tile/accordion cycling, simple left/up container joins, ten numeric workspaces, sequential workspace navigation, and move-then-follow shortcuts.

All runtime behaviors and bindings are Maintainer Preferences. `config-version = 2` is instead an explicit compatibility declaration recommended by current official guidance. The file intentionally omits default normalization, layout, orientation, gap, auto-reload, focus-follows-mouse, key-mapping, persistent-workspace, and empty callback values. Scalar-like settings inherit official defaults, but bindings do not: `[mode.main.binding]` is a complete table, so essential bindings remain explicit even when they resemble the official sample.

The source configuration's WezTerm and browser launchers, fixed primary/secondary workspace assignments, WeChat and QQ routing, Shottr and Finder rules, title-based settings-window rule, and commented alternatives are not included. They depend on installed applications, monitor topology, language-sensitive titles, or personal workflow. Current AeroSpace releases also include [improved dialog and browser picture-in-picture heuristics](https://github.com/nikitabobko/AeroSpace/releases/tag/v0.20.0-Beta), so the old broad picture-in-picture rule is no longer presented as generally necessary.

## Known conflicts

Option-based global shortcuts can conflict with macOS text input or other hotkey tools, especially Raycast, Karabiner-Elements, skhd, and application shortcuts. `automatically-unhide-macos-hidden-apps` removes ordinary Cmd-H behavior. Pointer movement on every focus change can be distracting and should be reassessed before enabling `focus-follows-mouse`. The `--focus-follows-window` move commands switch visible workspace; remove the flag when windows should move without following them.

Do not infer monitor assignments or application routing from this reference. Discover current monitor names and application bundle identifiers in the user's own environment before proposing either feature.

## Safe validation

First parse the candidate as TOML without contacting the running application.
Replace `<candidate-path>` with whichever of the two supported paths is active:

```sh
python3 -c 'import sys, tomllib; tomllib.load(open(sys.argv[1], "rb"))' '<candidate-path>'
```

After the accepted configuration is at AeroSpace's active target path, validate its semantics without reloading it:

```sh
aerospace reload-config --dry-run --no-gui --warnings-as-errors
```

The dry run reports configuration errors without applying the candidate. If it fails, stop and offer the established Recovery Path. A real reload, application launch, Accessibility change, login-item change, or window rearrangement has effects and requires confirmation.

## Consumer AI workflow

Follow the repository workflow in `AGENTS.md`. In particular, inspect both supported target paths, the active AeroSpace version, Accessibility permission, existing global shortcuts, monitor topology, and any current application-routing rules before planning. Present only the smallest selected capabilities and explain which default-derived lines were omitted. Establish a Git checkpoint or exact single-file backup before editing, validate safely, and then record the user's current goal, reasons, and Review Cursor in comments or a nearby intent document.

When reviewing a newer repository version, run `scripts/update-context <Review-Cursor> aerospace`, compare only the AeroSpace changes with the user's environment and current intent, and ask before applying any behavior, dependency, or Maintainer Preference change.
