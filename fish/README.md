# Fish

## Purpose

This module is one coherent, deliberately small Fish Reference Configuration. A user's AI should select and adapt only the capabilities that serve the user's stated goal; it should not replace an existing configuration wholesale.

## Applicable environment

The reference was validated with Fish 4.9.2 on macOS 26.6.2 and with the official Fish 4.9.2 standalone binary on Linux x86-64 in CI. It uses Fish built-ins and is expected to be portable across Fish 4.x environments, but other versions and operating systems must be inspected rather than assumed compatible.

## Prerequisites and installation

Fish is required. Detect it with `command -v fish` and inspect its version with `fish --version`. The official project and installation documentation are at https://fishshell.com/.

On macOS, `brew install fish` is an optional installation path when the user has chosen Homebrew. Explain a missing installation and ask for explicit approval before running that or any other installation command.

Git is optional. Detect it with `command -v git`. The configuration adds the `gst` abbreviation only when Git already exists; the abbreviation is not a reason to install Git.

## Target configuration location

The reference `config.fish` corresponds to `$XDG_CONFIG_HOME/fish/config.fish`. When `XDG_CONFIG_HOME` is unset, Fish uses `~/.config/fish/config.fish`.

Inspect the actual Fish configuration directory and existing file before proposing changes. Merge accepted capabilities into that file while preserving unrelated content; do not assume the entire reference belongs there.

## Included capabilities

- Interactive-only scoping prevents presentation preferences from affecting non-interactive Fish processes.
- An empty `fish_greeting` starts interactive shells quietly.
- When Git is already available, `gst` expands to `git status --short --branch`.

The comments in `config.fish` identify the conditions and choices closest to the settings they describe.

## Maintainer Preferences

The quiet greeting and `gst` abbreviation are subjective choices, not Reusable Rules. Present them separately and adopt either one only when it matches the user's intent.

## Known conflicts

An existing `fish_greeting` customization conflicts with the quiet greeting. An existing abbreviation, alias, or function named `gst` conflicts with the reference abbreviation. Preserve the user's existing behavior unless they explicitly choose the reference behavior after seeing the impact.

Fish loads `conf.d/*.fish` before `config.fish`; inspect those files when a value or abbreviation appears to come from elsewhere.

## Safe validation

Run syntax validation before loading the changed configuration:

```sh
fish --no-config --no-execute "${XDG_CONFIG_HOME:-$HOME/.config}/fish/config.fish"
```

This parses the file without executing its commands. If it fails, stop, show the diagnostic, and use the established Recovery Path. Starting or restarting an interactive shell can affect the user's session and requires confirmation.

## Consumer AI workflow

1. Understand the desired Fish behavior and unresolved choices.
2. Inspect the operating system, Fish version, resolved configuration directory, existing `config.fish`, relevant `conf.d` files, and whether Git and conflicting names exist.
3. Read this module and the capability comments in `config.fish`.
4. Present a minimal plan covering exact edits, behavior, conflicts, optional dependencies, recovery, and validation. Do not edit yet.
5. Obtain confirmation for each behavior change. If Fish or Git is missing, do not install it unless the user separately approves an official source or their chosen package manager.
6. Establish a Recovery Path, then merge only the accepted capabilities and preserve unrelated settings. Prefer an existing version-control checkpoint. If an existing target is not version-controlled, create a sibling backup before editing, tell the user its exact path, and provide the exact command that would restore it. If the target does not exist yet, record that prior absence and explain that recovery removes the newly created file. Never apply either restoration without confirmation.
7. Run the safe syntax validation above. On failure, stop and offer restoration; do not continue to shell restart or further changes.
8. On success, update the user's existing intent document with the current goal, reasons for non-obvious choices, and the upstream release or commit reviewed. If no convention exists, prefer useful comments in `config.fish`; when a companion document is clearer, propose `AI-INTENT.md` in the Fish configuration directory and ask before creating it.

The intent record belongs to the user's Consumer Configuration, not this repository. It must not contain credentials. A later AI session reads it before proposing further Fish changes.
