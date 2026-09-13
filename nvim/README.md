# Neovim

## Purpose and environment

This module is the maintainer's deliberately small LazyVim-based Neovim configuration. It was validated with Neovim 0.12.5, LazyVim 16.0.1, lazy.nvim 11.17.5, and Tree-sitter CLI 0.27.0 on macOS 26.6.2, and records LazyVim configuration format version 8. It enables the LazyVim defaults, C/C++ through Clangd, Rust, TOML, and an opinionated transparent Catppuccin Mocha theme.

## Prerequisites and installation

This reviewed lock checkpoint requires Neovim 0.12 or newer because it follows the rewritten `main` branch of nvim-treesitter. Detect the commands and versions below before proposing startup. Install Neovim using its official installation documentation at https://neovim.io/doc/user/starting.html#install and review LazyVim's official installation guidance at https://www.lazyvim.org/installation. The official lazy.nvim configuration reference is https://lazy.folke.io/configuration.

Dependencies are scoped to the selected capability:

| Capability or file | Exact dependency | Detection and acquisition behavior |
| --- | --- | --- |
| LazyVim bootstrap and every locked plugin | [Git](https://git-scm.com/downloads) plus network access to GitHub | `lua/config/lazy.lua` clones `folke/lazy.nvim`, then lazy.nvim downloads the plugins named by LazyVim and `lazy-lock.json` on first startup. No plugin is vendored. Inspect `git --version` and obtain confirmation before that network/filesystem mutation. |
| LazyVim/Mason downloads and native plugin builds | [curl](https://curl.se/download.html), a platform `tar`, and a C compiler | Check `curl --version`, `tar --version`, and `cc --version`. On the tested macOS environment, Apple provides `tar` and the compiler through [Xcode Command Line Tools](https://developer.apple.com/xcode/resources/); other platforms should use their official system toolchain. These tools support installation/build steps and are not needed for parse-only validation. |
| nvim-treesitter parser installation | [Tree-sitter CLI](https://github.com/tree-sitter/tree-sitter) 0.26.1 or newer plus a C compiler | Check `tree-sitter --version` and `cc --version`. Use an official binary or system package rather than npm as required by the reviewed nvim-treesitter generation; parser installation and `:TSUpdate` require approval. |
| Catppuccin Mocha theme | [`catppuccin/nvim`](https://github.com/catppuccin/nvim) | The plugin is declared in `lua/plugins/colorscheme.lua` and downloaded automatically by lazy.nvim; do not ask the user to install a separate Neovim theme package. `habamax` is the built-in recovery fallback. |
| C/C++ editing | `clangd` from the [LLVM project](https://clangd.llvm.org/installation), plus the plugins in LazyVim's [Clangd extra](https://www.lazyvim.org/extras/lang/clangd) | Check `clangd --version`. The extra configures the server and can let Mason install it; either Mason installation or system installation requires separate approval. `codelldb` is additionally needed only when C/C++ debugging is selected. |
| Rust editing | `rust-analyzer`, normally installed through [rustup](https://rust-analyzer.github.io/manual.html#rustup), plus the plugins in LazyVim's [Rust extra](https://www.lazyvim.org/extras/lang/rust) | Check `rust-analyzer --version`. The extra reports when it is absent and can let Mason install `codelldb` for debugging; language-server and debugger installation require separate approval. |
| TOML editing | LazyVim's [TOML extra](https://www.lazyvim.org/extras/lang/toml) | The reviewed extra only configures LazyVim's existing LSP layer and introduces no separately required executable. Recheck its official page when updating LazyVim. |
| `stylua.toml` formatting policy | [StyLua](https://github.com/JohnnyMorganz/StyLua), only when Lua formatting is selected | Check `stylua --version`. The TOML file is inert without StyLua; installing or enabling the formatter requires approval. |
| LazyVim interface icons | Any installed [Nerd Font](https://www.nerdfonts.com/font-downloads) | Optional rendering aid, not a requirement of this configuration. Verify glyphs in the user's terminal or GUI and let the user choose the family; no font is installed automatically. |

Language tooling is optional until the matching capability is used. LazyVim or Mason may offer to install tools, but that offer does not authorize installation.

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
