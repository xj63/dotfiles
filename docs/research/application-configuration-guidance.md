# Official application configuration guidance

Research date: 2026-09-07.

This report checks the repository's Fish, WezTerm, Neovim/LazyVim, Starship,
and Zed reference configurations against first-party documentation and source.
It is implementation input, not a second configuration contract. Defaults are
version-sensitive: the findings below target the versions named by the modules
(Fish 4.9.2, WezTerm `20240203-110809-5046fc22`, Neovim 0.12.5 with LazyVim
format 8, Starship 1.26.0, and Zed 1.18.1). Recheck upstream defaults whenever
those versions change.

## Cross-application authoring conclusion

The reference files should retain only settings that express an intentional
departure from the applicable upstream default. An explicit default is useful
only when it deliberately freezes behavior against future upstream changes; in
that case its comment must say that this is the intent. Comments should explain
the goal, observable effect, prerequisites, and important conflict of the
setting they accompany—not merely restate its syntax.

Comment support differs by file type:

- Fish supports `#` through end-of-line and has no multiline comment syntax;
  its manual explicitly recommends comments for explaining what and why
  ([Fish language: Comments](https://fishshell.com/docs/current/language.html#comments)).
- WezTerm and Neovim configuration are Lua and support `--` line comments and
  `--[[...]]` block comments. The official configurations themselves use line
  comments extensively ([WezTerm configuration files](https://wezterm.org/config/files.html),
  [Neovim Lua guide](https://neovim.io/doc/user/lua-guide.html)).
- Starship and StyLua use TOML, whose `#` comments are used throughout their
  official examples ([Starship configuration](https://starship.rs/config/),
  [StyLua configuration](https://github.com/JohnnyMorganz/StyLua#configuration)).
- Zed parses its own `settings.json` and `keymap.json` as JSONC. Its official
  default settings map those paths to JSONC, and official keymap examples use
  `//` comments ([Zed 1.18.1 default settings source](https://github.com/zed-industries/zed/blob/v1.18.1/assets/settings/default.json),
  [Zed keybindings](https://zed.dev/docs/key-bindings)). Therefore these two
  files can and should carry local intent comments despite their `.json`
  suffix. By contrast, Neovim's `lazyvim.json` and `lazy-lock.json` are JSON and
  should remain comment-free; explain their intent in adjacent Lua or README
  prose.

## Fish 4.9.2

### Startup behavior and corrections

Fish runs `conf.d/*.fish` before the user's `config.fish`, and runs both for
interactive and non-interactive shells. Presentation and prompt integrations
must therefore be guarded with `status is-interactive`
([Fish configuration files](https://fishshell.com/docs/current/language.html#configuration-files)).
The repository currently guards `fish_vi_key_bindings` and `gst`, but not
`conf.d/integrations.fish` or `conf.d/theme.fish`. FZF shell bindings, Starship,
Zoxide, and theme variables are interactive UI behavior and should be placed
behind that guard.

`abbr --add --global` is accepted by the tested binary as a compatibility/no-op
form, but `--global` is not part of the documented Fish 4.9 command interface.
Abbreviations stopped being stored as universal variables in Fish 3.6 and are
defined for each process by startup configuration. The declaration should use
the documented form `abbr --add gst 'git status --short --branch'`. An
abbreviation expands visibly in the editable command line rather than acting as
an alias
([Fish `abbr`](https://fishshell.com/docs/current/cmds/abbr.html)).

`fish_add_path` is idempotent, prepends by default, ignores nonexistent
directories, and—unless a global `fish_user_paths` already exists—writes the
universal `fish_user_paths`. That persistent state can survive removal of the
line that created it. File-owned path declarations should use
`fish_add_path --global ...` so removing the configuration also removes its
effect on the next shell; document the precedence because prepending may shadow
system binaries ([Fish `fish_add_path`](https://fishshell.com/docs/current/cmds/fish_add_path.html)).

### Meaning, defaults, and conflicts

- Fish defaults to Emacs-style editing. `fish_vi_key_bindings` is a meaningful
  preference, initially enters insert mode, and resets existing bindings unless
  `--no-erase` is used. Its comment should disclose that conflict and point
  users with custom bindings toward `fish_user_key_bindings`
  ([Fish vi mode](https://fishshell.com/docs/current/interactive.html#vi-mode-commands)).
- The greeting override is supported and only called interactively. The current
  function exposes the runtime hostname on screen (it does not store the host in
  the repository), which should be an explicit privacy/usability choice
  ([Fish configurable greeting](https://fishshell.com/docs/current/interactive.html#configurable-greeting)).
- One function per `functions/<name>.fish` uses Fish's preferred autoloading
  model. `--description` supplies completion/help text, and `--wraps` inherits
  completions; those annotations should say when the wrapped executable is
  optional and what failure to expect
  ([Fish autoloading functions](https://fishshell.com/docs/current/tutorial.html#autoloading-functions),
  [Fish `function`](https://fishshell.com/docs/current/cmds/function.html)).
- `conf.d/theme.fish` is not Fish's default theme; it closely mirrors Fish's
  bundled Nord theme. The provenance should be stated explicitly. Compared with
  the official 4.9.2 Nord file, this copy adds `fish_color_match`, uses `normal`
  instead of `--reset` for `fish_color_normal`, changes pager-prefix foreground,
  and omits some bold attributes. Each deviation should either be intentional
  and explained or aligned with upstream
  ([Fish 4.9.2 Nord theme source](https://github.com/fish-shell/fish-shell/blob/4.9.2/share/themes/nord.theme),
  [syntax-highlighting variables](https://fishshell.com/docs/current/interactive.html#syntax-highlighting-variables)).

No ordinary Fish default is redundantly reasserted by the intended settings;
the important changes are invalid syntax, missing interactive guards, implicit
persistent path scope, and undocumented derivation from the bundled Nord theme.

### Installation, inspection, and validation

Use Fish's official installation choices rather than assuming Homebrew
([Getting Fish](https://github.com/fish-shell/fish-shell#getting-fish)). Useful
read-only inspection commands are `fish_config theme show`, `abbr --show`, and
`functions --details NAME`. `fish --no-config --no-execute FILE` parses without
executing the file and remains the correct deterministic validation primitive
([Fish command options](https://fishshell.com/docs/current/cmds/fish.html)).

## WezTerm `20240203-110809-5046fc22`

### Defaults and effective preferences

`wezterm.config_builder()` is appropriate: since 20230320 it detects unknown
configuration keys and reports a configuration error instead of silently
accepting a typo
([`wezterm.config_builder`](https://wezterm.org/config/lua/wezterm/config_builder.html)).
The `wezterm.target_triple` branch is also the supported way to condition on the
target platform
([`wezterm.target_triple`](https://wezterm.org/config/lua/wezterm/target_triple.html)).

The following repository settings are intentional, non-default preferences:

- `enable_tab_bar = false` differs from `true`
  ([default](https://wezterm.org/config/lua/config/enable_tab_bar.html)).
- `font_size = 14` differs from `12`
  ([default](https://wezterm.org/config/lua/config/font_size.html)).
- `window_background_opacity = 0.8` or `0.95` differs from `1.0`, and
  transparency may cost rendering performance
  ([opacity](https://wezterm.org/config/lua/config/window_background_opacity.html)).
- `macos_window_background_blur = 50` differs from `0`
  ([macOS blur](https://wezterm.org/config/lua/config/macos_window_background_blur.html)).
- macOS `window_decorations = "RESIZE"` differs from `"TITLE | RESIZE"` and
  removes the title bar while retaining resize borders. With the tab bar also
  hidden, moving the window requires the documented modifier-drag behavior
  ([window decorations](https://wezterm.org/config/lua/config/window_decorations.html)).
- `Catppuccin Mocha` is a built-in but non-default color scheme; a `colors`
  block would override parts of it, so preserve an existing user's explicit
  colors instead of combining blindly
  ([appearance](https://wezterm.org/config/appearance.html)).
- The explicit Monaspace/Menlo stack is non-default and depends on an installed
  font. Omitting `font` uses WezTerm's bundled portable default font stack
  ([fonts](https://wezterm.org/config/fonts.html)).

There are no simple default-value assignments to remove. There are, however,
two functional defects that comments alone cannot repair:

1. `kde_window_background_blur` was nightly-only and immediately deprecated in
   favor of `wayland_window_background_blur`. It is not supported by the tested
   stable release and `config_builder()` can reject it. Remove it for stable
   compatibility, or explicitly require an appropriate nightly build
   ([deprecated option](https://wezterm.org/config/lua/config/kde_window_background_blur.html)).
2. `win32_system_backdrop = "Tabbed"` requires Windows 11 build 22621 or later
   and `window_background_opacity < 1` (the documentation recommends `0` for the
   best result). The current Windows branch leaves opacity at its `1.0` default,
   so the requested backdrop is ineffective. Either add a documented compatible
   opacity or remove the backdrop
   ([Windows backdrop](https://wezterm.org/config/lua/config/win32_system_backdrop.html)).

### Installation, inspection, and validation

Use the official platform installation pages
([macOS](https://wezterm.org/install/macos.html),
[Linux](https://wezterm.org/install/linux.html)); the tested release is
identified in the [official changelog](https://wezterm.org/changelog.html#20240203-110809-5046fc22).
WezTerm supports both `$HOME/.wezterm.lua` and
`$XDG_CONFIG_HOME/wezterm/wezterm.lua`
([configuration files](https://wezterm.org/config/files.html)).
`wezterm --config-file FILE show-keys --lua` safely loads the configuration and
prints resolved key assignments; `wezterm --config-file FILE ls-fonts` also
reveals the selected font files and fallback resolution
([general CLI options](https://wezterm.org/cli/general.html),
[`show-keys`](https://wezterm.org/cli/show-keys.html),
[`ls-fonts`](https://wezterm.org/cli/ls-fonts.html)).

## Neovim 0.12.5, LazyVim format 8, and StyLua

### Bootstrap and lazy.nvim defaults

Neovim reads `init.lua` from `stdpath("config")`; `stdpath("data")` is the
correct location for installed plugin data. `--headless` suppresses the UI but
does not by itself make a startup side-effect-free
([Neovim startup and standard paths](https://neovim.io/doc/user/starting.html),
[Lua configuration](https://neovim.io/doc/user/lua-guide.html#lua-guide-config)).
The repository bootstrap is materially the official LazyVim starter: clone the
stable `lazy.nvim` branch, prepend it to `runtimepath`, import LazyVim and local
plugin specs, enable background update checks, and disable selected built-in
runtime plugins
([official LazyVim starter](https://github.com/LazyVim/starter/blob/main/lua/config/lazy.lua)).
That provenance should be recorded so future agents compare against upstream
before copying new starter boilerplate.

Against lazy.nvim's own defaults:

- `defaults.lazy = false` exactly repeats the default and can be removed unless
  the project explicitly wants to freeze eager loading for user plugins.
- `defaults.version = false` is behaviorally equivalent to the default
  `nil`—latest Git commit—but is also the explicit recommendation in the
  LazyVim starter because plugin release tags may lag. Keep it only with that
  rationale; the lock file still pins resolved commits.
- `checker.enabled = true` changes the default `false`; `notify = false` changes
  the checker default `true` and matters because the checker is enabled.
- `install.colorscheme` changes the fallback list; `habamax` is the built-in
  final fallback, while Catppuccin is the intended first choice.
- Every named `performance.rtp.disabled_plugins` entry is effective because the
  default list is empty. Their comments should explain the lost capability
  (compressed-file editing for `gzip`/`tarPlugin`/`zipPlugin`, HTML conversion
  for `tohtml`, and the tutorial for `tutor`).

These defaults and meanings are defined by
[lazy.nvim configuration](https://lazy.folke.io/configuration) and its
[versioning guide](https://lazy.folke.io/spec/versioning).

### LazyVim format and selected extras

LazyVim's current first-party source declares configuration format version 8;
`install_version` preserves which generation of defaults an existing install
started with, while `version` triggers JSON migration when it differs. Neither
field is application preference boilerplate and both should remain
([LazyVim config source](https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/init.lua)).
The `news` cursor is generated state rather than a reusable capability; unless
the template deliberately suppresses already-read release news, omit it from a
general reference and let the consumer own its cursor.

The three extras are opt-in capabilities, not redundant copies of their shown
defaults. Clangd adds C/C++ parser and LSP behavior and expects `clangd`; Rust
adds Rust tooling including `rust-analyzer` and optional debugger installation;
TOML adds its language integration. Their official pages explicitly warn not to
copy the displayed plugin defaults into user configuration
([Clangd extra](https://www.lazyvim.org/extras/lang/clangd),
[Rust extra](https://www.lazyvim.org/extras/lang/rust),
[TOML extra](https://www.lazyvim.org/extras/lang/toml)).

The Catppuccin plugin defaults `transparent_background` to `false`; the
repository's `true` is therefore a real preference that delegates visible
background color to the terminal/GUI and can affect floating/plugin windows.
The plugin `name`, priority, and LazyVim colorscheme override are needed to make
the selected scheme load predictably
([Catppuccin Neovim configuration](https://github.com/catppuccin/nvim#configuration)).

In `stylua.toml`, `column_width = 120` repeats StyLua's official default and can
be removed unless it intentionally freezes the width. `indent_type = "Spaces"`
and `indent_width = 2` differ from the defaults (`Tabs`, width 4) and express
the real formatting preference
([StyLua configuration defaults](https://github.com/JohnnyMorganz/StyLua#configuration)).

### Installation, inspection, and validation

Neovim's official entry point is [neovim.io](https://neovim.io/); LazyVim's
requirements include a sufficiently new Neovim, Git, a C compiler for
Tree-sitter, and an optional Nerd Font
([LazyVim installation](https://www.lazyvim.org/installation)).
Syntax-only validation should continue to load each Lua file with `nvim
--clean --headless -u NONE` and parse both JSON files separately. An actual
startup can clone or update plugins and write data/state, so it requires user
approval. After approval, `:checkhealth`, `:LazyHealth`, and `:Lazy` are the
first-party inspection surfaces; Neovim documents `:checkhealth` as the standard
plugin/environment diagnostic
([Neovim health checks](https://neovim.io/doc/user/lua-plugin.html#health)).

## Starship 1.26.0

### Provenance, defaults, and behavior

The repository configuration is a modified version of Starship's official Pure
preset. It keeps Pure's compact Git formatting and styles, moves contextual
modules to `right_format`, changes character colors, and omits Pure's Python
detection overrides. State that provenance above `format`
([Pure preset](https://starship.rs/presets/pure-preset)).

Only one current assignment exactly repeats a Starship default:
`[git_state].format = '\([$state( $progress_current/$progress_total)]($style)\) '`. Remove it and retain the non-default `style = "bright-black"`, unless freezing
the upstream format is explicitly intended
([Git state defaults](https://starship.rs/config/#git-state)).

All other assignments are effective departures from defaults: the explicit
left `format` replaces `$all`; `right_format` replaces an empty right prompt;
directory style changes bold cyan to blue; character symbols/colors change;
and the Git branch/status, command duration, and Python formats/styles are
customized. The official module reference contains the exact defaults
([Starship configuration](https://starship.rs/config/)).

Important intent and conflict notes:

- The zero-width Git markers intentionally collapse conflicted, untracked,
  modified, staged, renamed, and deleted states into one `*` group. It omits
  `typechanged`, while Starship's `$all_status` includes that category, and it
  removes per-category symbols/count visibility. Ahead/behind retain their
  defaults and stash becomes `≡`
  ([Git status](https://starship.rs/config/#git-status)).
- The displayed Python format uses only `$virtualenv`, but leaving module
  detection at its defaults still activates Python and can perform version
  detection for Python files/projects. The official Pure preset sets
  `detect_extensions = []` and `detect_files = []` so it activates only for a
  virtual environment. Restore those two lines if “active virtual environment
  only” is the goal
  ([Python module](https://starship.rs/config/#python)).
- Putting `$username` and `$hostname` in `format` does not make them universally
  visible. Username defaults to root, a differing user, or SSH; hostname
  defaults to SSH only. Explain both the conditional behavior and possible
  identity disclosure
  ([username](https://starship.rs/config/#username),
  [hostname](https://starship.rs/config/#hostname)).
- A right prompt is supported in Fish and several other shells, while Bash
  needs Ble.sh 0.4 or newer. It may be hidden or crowded in narrow terminals
  ([right prompt](https://starship.rs/advanced-config/#enable-right-prompt)).

### Installation, inspection, and validation

Use the [official installation and shell initialization guide](https://starship.rs/guide/#-installation)
and the [v1.26.0 release](https://github.com/starship/starship/releases/tag/v1.26.0).
`STARSHIP_CONFIG=FILE starship print-config` parses and resolves a candidate;
`starship explain` explains currently visible modules, `starship timings`
identifies slow modules, and `STARSHIP_LOG=trace starship module NAME` diagnoses
one module ([Starship FAQ](https://starship.rs/faq/)).

## Zed 1.18.1

### Defaults that should not be repeated

The official default file is the most precise first-party source for nested
settings and is itself heavily commented
([Zed 1.18.1 default settings](https://github.com/zed-industries/zed/blob/v1.18.1/assets/settings/default.json)).
For the repository's current settings, these assignments repeat the upstream
default and should be removed unless their comments explicitly say the template
is freezing that default:

- `project_panel.dock = "right"`, `outline_panel.dock = "right"`,
  `collaboration_panel.dock = "right"`, and `git_panel.dock = "right"`;
- `theme.mode = "system"` is the default mode, although keeping it beside the
  non-default light and dark Catppuccin choices makes the combined intent clear.

All other repository entries are effective choices: CLI `new_window` differs
from `existing_window`; Git tree view differs from `false`; Catppuccin
icon/themes and Monaspace differ from Zed defaults; Vim mode, wrapped relative
numbers, focus-change autosave, minimap auto mode, inlay hints, inline
diagnostics, and signature help all change their disabled/off defaults. Quit
confirmation, close-panel-on-toggle, smart-case search, and editor sticky scroll
change `false` defaults to `true`; the six-line vertical scroll margin changes
the default `3`; and Markdown editor-width wrapping overrides the language
default of no soft wrapping. Telemetry changes both `true` defaults to `false`;
the file association and CargoTom initialization option are
environment-dependent additions. Exact scalar defaults are also collected in the
[All Settings reference](https://zed.dev/docs/reference/all-settings).

### Conditions and conflicts requiring comments

- `cli_default_open_behavior = "new_window"` changes CLI and double-click
  behavior, not File > Open
  ([Windows and projects](https://zed.dev/docs/windows-and-projects)).
- `autosave = "on_focus_change"` saves when moving focus away from a buffer;
  it can trigger formatters or other save hooks
  ([autosave setting](https://zed.dev/docs/reference/all-settings#autosave)).
- Inlay hints require support from each language server and may need additional
  server configuration
  ([inlay hints](https://zed.dev/docs/reference/all-settings#inlay-hints)).
- `confirm_quit = true` prevents accidental whole-application exit but adds an
  interaction to deliberate or scripted quits. `close_panel_on_toggle = true`
  turns a focused panel shortcut into a close action rather than only returning
  focus to the editor.
- Smart-case search treats uppercase queries as case-sensitive. Editor sticky
  scroll and a larger vertical margin preserve navigation context but consume
  additional height in short panes.
- Markdown `soft_wrap = "editor_width"` is a visual language-specific override;
  it neither inserts newlines nor changes wrapping for source-code languages
  ([language-specific settings](https://zed.dev/docs/configuring-languages)).
- The CargoTom setting requires the third-party extension; its official Zed
  gallery page confirms the extension but does not document
  `hide_docs_info_message`, so the repository must describe that option as
  extension-specific and verify it against the installed extension version
  rather than presenting it as a Zed core setting
  ([CargoTom gallery entry](https://zed.dev/extensions/cargo-tom)).
- `shift shift` is explicitly supported and fires on modifier release. In
  `Workspace` context it applies throughout Zed and may conflict with OS/input
  methods or another binding. Later user bindings at the same context take
  precedence
  ([keybinding syntax and precedence](https://zed.dev/docs/key-bindings)).
- Catppuccin Blur themes/icons and Monaspace are installed resources, not core
  defaults. Zed's extension UI must be used to confirm/install themes, and the
  font must exist on the system
  ([installing extensions](https://zed.dev/docs/extensions/installing-extensions),
  [font setting](https://zed.dev/docs/reference/all-settings#buffer-font-family)).

### Installation, inspection, and validation

Use the official [Zed download](https://zed.dev/download). On macOS/Linux the
configuration paths are `~/.config/zed/settings.json` and `keymap.json`
([Zed FAQ](https://zed.dev/faq)); the CLI is installed from the command palette
on macOS and `zed --version` reports the application version
([Zed CLI reference](https://zed.dev/docs/reference/cli)).

Strict `python -m json.tool` is too restrictive once the template restores
supported JSONC comments. Prefer a JSONC-aware parser or Zed's schema diagnostics
for deterministic checking. In Zed, open Default Settings to compare inherited
values, use the Settings Editor/schema diagnostics for unsupported fields, use
the keymap editor and `dev: open key context view` for binding conflicts, and
use `zed: open log` for extension/LSP diagnostics. Opening or reloading the app,
installing extensions remains consequential and requires confirmation.
