# AeroSpace configuration research

Research date: 2026-09-08.

This report compares the maintainer's existing AeroSpace configuration with
first-party documentation and source. The local file was used only to identify
behaviors and defaults; machine-specific values are intentionally not recorded
here. This is implementation input, not a second configuration contract.

## Version and source of truth

AeroSpace has no GitHub release marked stable: every published release returned
by the official repository is a prerelease. The newest release as of the
research date is [`v0.21.3-Beta`](https://github.com/nikitabobko/AeroSpace/releases/tag/v0.21.3-Beta),
published on 2026-07-16. The module should therefore say "latest published beta"
rather than "latest stable" and pin its research and validation expectations to
`v0.21.3-Beta`.

The exact upstream configuration baseline for that release is the tagged
[`default-config.toml`](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/config-examples/default-config.toml).
Do not use `main` as the baseline for a versioned module. The currently installed
application reports `0.19.2-Beta`, so it cannot validate newer options such as
`config-version = 2`, `auto-reload-config`, or the new dry-run validation flag.
Upgrade before validating a configuration targeted at `0.21.3-Beta`.

## Environment, installation, and target location

AeroSpace is an i3-like tiling window manager for macOS. The tagged project
README supports the release binary on macOS 13 or newer, on Apple Silicon and
Intel Macs ([compatibility source](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/README.md#macos-compatibility-table)).
It operates through the public macOS Accessibility API, so users must grant the
application Accessibility permission
([project design](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/README.md#values)).

The official preferred installation is:

```sh
brew install --cask nikitabobko/tap/aerospace
```

Manual installation is also supported from the
[`v0.21.3-Beta` release assets](https://github.com/nikitabobko/AeroSpace/releases/tag/v0.21.3-Beta).
The application is required; putting the bundled `aerospace` binary on `PATH` is
optional for ordinary use but required for the recommended inspection and
validation commands
([installation guide](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/guide.adoc#installation)).

AeroSpace checks exactly two user configuration locations, in order:

1. `~/.aerospace.toml`
2. `${XDG_CONFIG_HOME}/aerospace/aerospace.toml`, with `XDG_CONFIG_HOME`
   defaulting to `~/.config`

If both exist, AeroSpace reports ambiguity. A module may use a native root file
named `.aerospace.toml`, but its README must tell a consumer AI to copy it to one
of these locations and avoid creating both
([configuration locations](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/guide.adoc#custom-config-location)).

The syntax is TOML 1.1.0. Comments use `#`. Scalar-like omitted values generally
inherit the upstream default, but vector-like values generally fall back to an
empty array or table. Important explicit exceptions are bindings,
`on-focused-monitor-changed`, and `exec`
([default fallback rules](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/guide.adoc#default-config)).

## Defaults found in the maintainer configuration

These are the effective fallback values for keys in or closely related to the
maintainer configuration. The distinction between scalar and collection
fallbacks is essential when reducing copied boilerplate:

| Key | Effective fallback in `v0.21.3-Beta` | Treatment |
| --- | --- | --- |
| `config-version` | `1` | Add `2`; it is the recommended compatibility contract. |
| `after-login-command` | deprecated; only `[]` is accepted | Remove. |
| `after-startup-command` | `[]` | Retain only non-empty intentional startup actions. |
| `start-at-login` | `false` | `true` is a Maintainer Preference. |
| `auto-reload-config` | `false` | Omit unless automatic reload is intentionally wanted. |
| `enable-normalization-flatten-containers` | `true` | Remove copied default. |
| `enable-normalization-opposite-orientation-for-nested-containers` | `true` | Remove copied default. |
| `accordion-padding` | `30` | Remove copied default. |
| `default-root-container-layout` | `tiles` | Remove copied default. |
| `default-root-container-orientation` | `auto` | Remove copied default. |
| `on-focus-changed` | `[]` | Retain only intentional callback. |
| `on-focused-monitor-changed` | `[]` | Retain only intentional callback. |
| `automatically-unhide-macos-hidden-apps` | `false` | `true` is a preference that changes Hide behavior. |
| `persistent-workspaces` with config version 2 | `[]` | Omit unless empty workspaces must stay alive. |
| `focus-follows-mouse.enabled` | `false` | Omit unless enabled. |
| `key-mapping.preset` | `qwerty` | Remove copied default. |
| all six gap values | `0` | Remove copied defaults. |
| `workspace-to-monitor-force-assignment` | `{}` | Any mapping is hardware/workflow-specific. |
| `on-window-detected` | `[]` | Every rule is intentional and ordered. |
| `mode.*.binding` | `{}` | Every desired binding must remain explicit. |

These values are defined in the tagged
[`default-config.toml`](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/config-examples/default-config.toml).

The existing empty `after-login-command` should also be removed. The parser
accepts an empty array only for migration compatibility; any non-empty value is
an error because the option has been deprecated since 0.19.0
([tagged parser](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/Sources/AppBundle/config/parseConfig.swift#L179-L185)).
`after-startup-command` is its supported replacement when startup behavior is
actually desired
([startup callback guide](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/guide.adoc#after-startup-command)).

Two categories must **not** be removed merely because their lines resemble the
official default file:

- `mode.*.binding` falls back to an empty table. A custom config is the complete
  source of truth for its bindings, so every desired binding must remain
  explicit.
- `on-focused-monitor-changed` falls back to an empty command list. Retain the
  mouse movement command if it is part of the intended behavior.

`on-focus-changed`, `workspace-to-monitor-force-assignment`, and
`on-window-detected` likewise default to no callbacks or assignments. Every
retained entry is therefore an intentional behavior, not default boilerplate.
`config-version = 2` should be added: omission selects version 1, while version
2 is the highest supported and recommended version and makes
`persistent-workspaces` explicitly default to an empty array
([config version](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/guide.adoc#config-version)).

## Recommended reusable reference

The reference can preserve a coherent, numbered-workspace, Vim-directional
workflow while removing copied defaults. These non-default behaviors are useful
as a general reference when each is explained next to the setting:

- Start AeroSpace at login. This is convenient but changes login behavior, so
  label it as a Maintainer Preference rather than a prerequisite.
- Select a known workspace after AeroSpace starts. This is deterministic but
  steals workspace focus at startup; keep it only as a preference.
- Move the pointer lazily to newly focused windows or monitors. These callbacks
  are useful in keyboard-driven navigation but may surprise mouse users and
  should be independently removable
  ([focus callbacks](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/guide.adoc#on-focus-changed-callbacks)).
- Automatically unhide macOS-hidden applications. This prevents accidental
  Command-H state from fighting the window manager, but intentionally changes
  native Hide behavior
  ([official rationale](https://nikitabobko.github.io/AeroSpace/goodies#disable-hide-app)).
- Keep explicit directional focus and move bindings, numeric workspace
  selection, numeric move-to-workspace bindings, resizing, floating/fullscreen
  toggles, layout toggling, and `join-with` nesting shortcuts. Even assignments
  equal to the default sample must remain because bindings never inherit.
- Keep `--focus-follows-window` on move-to-workspace only if the intended flow is
  to follow the moved window. The flag explicitly focuses the destination window
  after a successful move
  ([command reference](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/aerospace-move-node-to-workspace.adoc)).
- Keep a generic Picture-in-Picture floating rule, but describe title matching
  as best effort: the official guide warns that some titles are initialized only
  after window detection
  ([callback guide](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/guide.adoc#on-window-detected-callback)).
- A generic Finder-floating rule can be an optional Maintainer Preference. It
  affects every Finder window, not only transient dialogs, and should say so.

## Local or conditional behavior to omit from the general reference

The following behavior reflects the maintainer's installed applications or
hardware and should not be active in a general reference configuration:

- shortcuts that launch a particular terminal or browser;
- rules that route particular chat applications to a chosen workspace;
- rules for a particular screenshot utility;
- a fixed workspace-to-main/secondary-monitor assignment.

If any of these are worth teaching, show them only as commented examples with
placeholders and explicit prerequisites. A main/secondary assignment assumes a
two-monitor topology and prevents `move-workspace-to-monitor` from moving the
assigned workspace
([monitor assignment semantics](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/guide.adoc#assign-workspaces-to-monitors)).

The broad localized "settings" title regex is also risky as a default: it can
float unrelated documents or pages and can miss windows whose title arrives
late. Prefer a bundle-ID match plus a narrower condition, or omit it from the
reference and explain how a consumer AI can add an application-specific rule.

## Binding and migration details

The local binding set is internally coherent because it reserves letters for
window-management or launcher actions and uses numeric workspaces. It does not
need to reproduce the upstream A-Z workspace bindings. Important differences
from the latest default sample should be documented as choices:

- sequential next/previous workspace navigation replaces upstream
  back-and-forth and move-workspace-to-monitor behavior;
- one layout binding toggles tiles and accordion while the upstream sample uses
  separate layout/orientation behavior;
- directional `join-with` bindings construct nested containers and are the
  preferred high-level alternative to `split`
  ([`join-with`](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/aerospace-join-with.adoc));
- using a letter for an application launcher or floating toggle means that the
  same letter is intentionally unavailable for a letter-named workspace.

Binding modes are mutually exclusive: AeroSpace starts in `main`, and switching
mode deactivates all bindings from the previous mode. A second resize/service
mode is optional rather than required
([binding modes](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/guide.adoc#binding-modes)).

The current `[[on-window-detected]]` entries use the legacy `if.*` matcher form.
It remains supported but is soft-deprecated. New reference content should use
the composable v0.21 syntax:

```toml
on-window-detected = [
  {
    if = 'test %{app-bundle-id} = <APP_BUNDLE_ID>',
    run = 'layout floating',
  },
]
```

Rules are ordered and stop after the first successful match unless
`check-further-callbacks = true` is set. This is important when combining a
generic floating rule with an app-routing rule. The syntax and ordering are
specified in the
[tagged callback guide](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/guide.adoc#on-window-detected-callback).
Use `aerospace list-apps` or `mdls -name kMDItemCFBundleIdentifier -r
/Applications/App.app` to discover bundle IDs from the user's own machine; do
not copy the maintainer's application list blindly
([official discovery guidance](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/aerospace-list-apps.adoc)).

## Inspection, validation, and reload

After upgrading to `v0.21.3-Beta`, use these safe checks:

```sh
aerospace --version
aerospace config --config-path
aerospace reload-config --dry-run --no-gui --warnings-as-errors
```

The last command parses the selected config, reports errors and warnings, exits
nonzero for either, and does not reload it. It is the preferred deterministic
validation command
([`reload-config` reference](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/aerospace-reload-config.adoc)).
`aerospace config --config-path` confirms which of the two possible files is
active
([`config` reference](https://github.com/nikitabobko/AeroSpace/blob/v0.21.3-Beta/docs/aerospace-config.adoc)).

Only after validation and user confirmation should an AI run:

```sh
aerospace reload-config --no-gui
```

Reloading changes active bindings, callbacks, login registration, and window
manager behavior. If validation fails, leave the active config untouched and
offer restoration from the user's version control or backup before proceeding.
