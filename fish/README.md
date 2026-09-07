# Fish

## Purpose

This module is a coherent Fish setup derived from the maintainer's daily configuration. It covers environment discovery, an opinionated interactive theme, and small command helpers. A user's AI should select only the capabilities that serve the stated goal; it should not replace an existing configuration wholesale.

## Applicable environment

The reference was validated with Fish 4.9.2 on macOS 26.6.2. Its core syntax uses Fish 4.x, while the Homebrew, Android Studio, and `open` conventions are macOS-specific and optional.

## Prerequisites and installation

Fish is required. Detect it with `command -v fish` and inspect its version with `fish --version`. Use Fish's official installation documentation at https://fishshell.com/docs/current/#installation. Read the official configuration-file and startup-order reference at https://fishshell.com/docs/current/language.html#configuration-files before moving settings between `conf.d`, functions, and `config.fish`.

On macOS, `brew install fish` is an optional installation path when the user has chosen Homebrew. Explain a missing installation and ask for explicit approval before running that or any other installation command.

Git, Neovim, Starship, FZF, Zoxide, Eza, Yazi, 7-Zip (`7zz`), uv, WezTerm, Android Studio, and its SDK are optional. The configuration detects startup integrations before loading them. Individual helper functions still report the missing command when invoked; never install an optional tool merely to satisfy this reference.

## Target configuration location

The reference `config.fish` corresponds to `$XDG_CONFIG_HOME/fish/config.fish`. When `XDG_CONFIG_HOME` is unset, Fish uses `~/.config/fish/config.fish`.

Inspect the actual Fish configuration directory and existing file before proposing changes. Merge accepted capabilities into that file while preserving unrelated content; do not assume the entire reference belongs there.

## Included capabilities

- Interactive-only scoping prevents editing preferences from affecting scripts.
- Vi key bindings and a dynamic time-and-host greeting shape interactive use.
- Fish's bundled Nord theme styles syntax highlighting and completion pages without committing generated color-variable output.
- Existing Homebrew, Rust, Android, and selected application paths are discovered without fixed usernames or SDK component versions.
- FZF, Starship, and Zoxide initialize only when installed.
- Directory, Python, archive, Yazi, uv, and WezTerm helpers keep common commands short; `ls` falls back to the system command when Eza is absent.
- `noproxy` clears common uppercase and lowercase proxy variables only for the current Fish process and its descendants; use it when a command must bypass a configured proxy.

The comments throughout `config.fish`, `conf.d`, and `functions` identify the intent, conditions, conflicts, and subjective choices closest to the settings they describe. The Nord selection is intentionally not a frozen palette: `fish_config theme choose Nord` loads the theme bundled with the installed Fish version, so upstream color changes may appear after a Fish upgrade.

## Maintainer Preferences

Vi bindings, the greeting, colors, Homebrew hint suppression, editor selection, and command wrappers are subjective choices, not Reusable Rules. Present them separately. The dependency guards, portable `$HOME` paths, and avoidance of pinned local SDK component versions are reusable safety rules.

## Known conflicts

Existing key bindings, theme variables, `fish_greeting`, `EDITOR`/`VISUAL`, Android or Java environment variables, and functions with the same names conflict with this reference. The `ls` wrapper is especially consequential because it replaces a core command; preserve the system behavior unless the user wants icons and Git state from Eza. Running `noproxy` can break network access that depends on a proxy, so invoke it explicitly rather than at startup and do not use it while proxy variables contain state that must remain in the current shell.

Fish loads `conf.d/*.fish` before `config.fish`; inspect those files when a value appears to come from elsewhere. Do not import `fish_variables`, generated completion links, proxy endpoints, account helpers, or credentials from another machine.

## Safe validation

Run syntax validation on every changed Fish file before loading the configuration:

```sh
find "${XDG_CONFIG_HOME:-$HOME/.config}/fish" -name '*.fish' -type f -exec fish --no-config --no-execute '{}' \;
```

This parses the files without executing their commands. If it fails, stop, show the diagnostic, and use the established Recovery Path. Starting or restarting an interactive shell can affect the user's session and requires confirmation.

## Consumer AI workflow

1. Understand the desired Fish behavior and unresolved choices.
2. Inspect the operating system, Fish version, resolved configuration directory, existing `config.fish`, `conf.d` and `functions` files, relevant optional tools, and conflicting names.
3. Read this module and the capability comments in `config.fish`, `conf.d`, and `functions`.
4. Present a minimal plan covering exact edits, behavior, conflicts, optional dependencies, recovery, and validation. Do not edit yet.
5. Obtain confirmation for each behavior change. If Fish or an optional tool is missing, do not install it unless the user separately approves an official source or their chosen package manager.
6. Establish a Recovery Path, then merge only the accepted capabilities and preserve unrelated settings. Inspect version control before editing. If the affected files are tracked and clean, record the current commit and an exact command such as `git restore --source=<checkpoint> -- <affected-path>`; if they already have changes, ask the user to commit them or approve another checkpoint rather than discarding them. If the target is not version-controlled, back up only the affected files, tell the user each exact backup path, and provide the exact command that would restore it. If the target does not exist yet, record that prior absence and explain that recovery removes the newly created file. Never apply any restoration without confirmation.
7. Run the safe syntax validation above. On failure, stop and offer restoration; do not continue to shell restart or further changes.
8. On success, update the user's existing intent document with the current goal, reasons for non-obvious choices, and the upstream release or commit reviewed. If no convention exists, prefer useful comments in `config.fish`; when comments are unsuitable, propose a Markdown document such as `AI-INTENT.md` inside the Fish configuration directory and ask before creating it. Use ignored `.local/` state in this clone only when intent cannot live beside the Consumer Configuration and the user approves that fallback.

Clone-local fallback state may record the Fish target location, current goal and reasons, and Review Cursor. It must not contain credentials, a copy of the Consumer Configuration, or backup contents. See [Private local fallback](../docs/local-consumer-state.md). A later AI session reads the selected intent record before proposing further Fish changes.

## Reviewing upstream changes

After the user asks to review a newer clone or release, read the existing Fish intent and run this read-only command from the knowledge-base clone:

```sh
scripts/update-context <Review-Cursor> fish
```

Use the reported `To` commit as the proposed next cursor. The command filters newly added change information and the tracked diff to Fish plus the shared consumer protocol; it also reports when the module was added or removed. It stops when the current cursor is not an ancestor of `To`, because a rollback or divergent history is not a valid update. The command does not inspect or modify the Consumer Configuration.

Compare every reported change with the user's current Fish files, current goal, environment, and selected capabilities. Produce a focused impact report that distinguishes behavior, dependency, Maintainer Preference, conflict, and documentation effects. The AI must not copy the newer Reference Configuration wholesale.

Ask before adopting any behavior, dependency, or Maintainer Preference change. If the user declines the update, keep both the Consumer Configuration and Review Cursor unchanged. For a partial acceptance, establish the Recovery Path, apply only the accepted changes, preserve unrelated and explicitly declined behavior, run safe validation, update the current intent and reasons, and advance the Review Cursor to the reported `To` commit. Advancing the cursor records that the entire range was reviewed, not that every upstream preference was adopted.
