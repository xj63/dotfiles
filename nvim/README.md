# Neovim

## Purpose and environment

This module is the maintainer's deliberately small LazyVim-based Neovim configuration. It was validated with Neovim 0.12.5 on macOS 26.6.2 and records LazyVim format version 8. It enables the LazyVim defaults, C/C++ through Clangd, Rust, TOML, and an opinionated transparent Catppuccin Mocha theme.

## Prerequisites and installation

Neovim, Git, and network access to GitHub are required for first-time bootstrap. Detect them with `command -v nvim`, `nvim --version`, and `command -v git`. Install Neovim from https://neovim.io/doc/user/ and review LazyVim's official installation guidance at https://www.lazyvim.org/installation. Language tooling such as Clangd and Rust Analyzer is optional until the matching language capability is used; LazyVim or Mason may offer to install additional tools.

Starting Neovim with this configuration can clone `lazy.nvim`, download plugins, update plugin metadata, and create files under Neovim's data and state directories. Explain these effects and obtain confirmation before the first launch. Do not infer permission to install language servers or formatters.

## Target configuration location

The module contents map to `$XDG_CONFIG_HOME/nvim`, falling back to `~/.config/nvim`. Inspect the existing directory, including its own version-control status, before proposing changes. Merge selected files rather than replacing an established plugin manager or distribution.

## Capabilities and maintainer preferences

`init.lua` delegates startup to `config.lazy`. The bootstrap loads LazyVim and local plugin specs, while `lazyvim.json` selects Clangd, Rust, and TOML extras. `lazy-lock.json` is a reproducibility checkpoint for the exact plugin revisions reviewed here.

LazyVim itself, the chosen language extras, automatic background update checks without notifications, disabled built-in runtime plugins, Catppuccin Mocha, and terminal-provided transparency are Maintainer Preferences. A user's AI should distinguish desired editing capabilities from the distribution and visual choices.

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
