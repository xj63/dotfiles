# Neovim

## Purpose and environment

This module is the maintainer's deliberately small LazyVim-based Neovim configuration. It was validated with Neovim 0.12.5, LazyVim 16.0.1, lazy.nvim 11.17.5, and Tree-sitter CLI 0.27.0 on macOS 26.6.2, and records LazyVim configuration format version 8. It enables the LazyVim defaults, C/C++ through Clangd, Rust, TOML, and an opinionated transparent Catppuccin Mocha theme.

## Prerequisites and installation

This reviewed lock checkpoint requires Neovim 0.12 or newer because it follows the rewritten `main` branch of nvim-treesitter. Git, `curl`, `tar`, Tree-sitter CLI 0.26.1 or newer, a C compiler, and network access to GitHub are required for bootstrap and parser installation; a Nerd Font is optional. Detect the commands and versions before proposing startup. Install Neovim using its official installation documentation at https://neovim.io/doc/user/starting.html#install, review LazyVim's official installation guidance at https://www.lazyvim.org/installation, and install Tree-sitter CLI from an official binary or system package rather than npm as directed by https://github.com/nvim-treesitter/nvim-treesitter. The official lazy.nvim configuration reference is https://lazy.folke.io/configuration. Language tooling such as Clangd and Rust Analyzer is optional until the matching language capability is used; LazyVim or Mason may offer to install additional tools.

Starting Neovim with this configuration can clone `lazy.nvim`, download plugins, update plugin metadata, and create files under Neovim's data and state directories. Explain these effects and obtain confirmation before the first launch. Do not infer permission to install language servers or formatters.

## Target configuration location

The module contents map to `$XDG_CONFIG_HOME/nvim`, falling back to `~/.config/nvim`. Inspect the existing directory, including its own version-control status, before proposing changes. Merge selected files rather than replacing an established plugin manager or distribution.

## Capabilities and maintainer preferences

`init.lua` delegates startup to `config.lazy`, which is intentionally derived from the official LazyVim starter rather than copied without provenance. The bootstrap loads LazyVim and local plugin specs. `lazyvim.json` uses LazyVim configuration format 8 and selects the official [Clangd](https://www.lazyvim.org/extras/lang/clangd), [Rust](https://www.lazyvim.org/extras/lang/rust), and [TOML](https://www.lazyvim.org/extras/lang/toml) extras. Its `version` and `install_version` fields drive LazyVim migrations; generated NEWS read-state is deliberately excluded. `lazy-lock.json` is a comment-free reproducibility checkpoint for the exact plugin revisions reviewed here.

LazyVim itself, the chosen language extras, automatic background update checks without notifications, disabled built-in runtime plugins, Catppuccin Mocha, and terminal-provided transparency are Maintainer Preferences. lazy.nvim's current-commit resolution is inherited rather than restated with the equivalent `defaults.version = false`; `defaults.lazy` is likewise omitted because `false` is already the default, and the lock file remains the deliberate reproducibility boundary. The nvim-treesitter plugin and its installed parsers form a compatible set: whenever an approved plugin update changes the locked nvim-treesitter revision, run its `:TSUpdate` build step rather than restoring the plugin alone. StyLua's default 120-column width is also omitted. The two-space formatting settings remain because they differ from StyLua's tab/four-space defaults. A user's AI should distinguish desired editing capabilities from distribution, update, and visual choices.

## Known conflicts

Do not combine this bootstrap unchanged with another plugin manager or Neovim distribution. Existing `init.lua`, `lua/config/lazy.lua`, `lazyvim.json`, lock files, colorscheme selection, runtime-path exclusions, or a plugin named `catppuccin` may conflict. Transparency depends on the terminal or GUI background. Lock-file commits can become unavailable or incompatible with a different Neovim/LazyVim version, so update them deliberately rather than deleting the lock without review.

## Safe validation

Compile every Lua file without executing the configuration or downloading plugins:

```sh
find "${XDG_CONFIG_HOME:-$HOME/.config}/nvim" -name '*.lua' -type f -exec nvim --clean --headless -u NONE -c "lua assert(loadfile('{}'))" -c qa \;
python3 -m json.tool "${XDG_CONFIG_HOME:-$HOME/.config}/nvim/lazyvim.json" >/dev/null
python3 -m json.tool "${XDG_CONFIG_HOME:-$HOME/.config}/nvim/lazy-lock.json" >/dev/null
```

These commands check syntax only. A headless startup with the actual `init.lua`, plugin synchronization, lock-file update, Mason installation, or interactive launch can access the network or modify state and requires confirmation.

After the user has approved bootstrap or an update, verify the installed runtime without changing plugin versions:

```sh
nvim --headless "+Lazy load nvim-treesitter" "+checkhealth lazyvim nvim-treesitter" +qa
```

An unloaded lazy plugin may appear to have no health provider, so load nvim-treesitter before requesting its dedicated health check. Stop on any real requirement, parser, or query error; do not treat a successful pull or lock-file change as proof that installed parsers are compatible.
