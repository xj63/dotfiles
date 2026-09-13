# Dependency-guidance acceptance

Date: 2026-09-13

The maintainer's local AI exercised the dependency-guidance addition to the Review Policy after `scripts/check all` passed. It reviewed only tracked repository content and current worktree changes; no Consumer Configuration, ignored local state, credentials, or backups were read.

- The synthetic “optional themes and fonts are required” wording was classified as Advisory because it did not name the resources, affected settings, detection method, installation behavior, or first-party sources.
- Fish now maps every external startup integration and command wrapper to its exact executable or installation path, explains when a missing tool matters, and records that Nord is bundled with Fish rather than supplied by a plugin.
- Zed now distinguishes the Catppuccin Blur theme extension from Catppuccin Icons, names the Monaspace Frozen Fonts package and exact family, and maps `lsp.cargo-tom` to CargoTom.
- Neovim now distinguishes automatically downloaded lazy.nvim plugins from external language servers, debuggers, StyLua, Tree-sitter tooling, and optional Nerd Font rendering.
- WezTerm now identifies the Monaspace Frozen Fonts package, explains the macOS-only Menlo fallback, and records that Catppuccin Mocha is bundled rather than a separate plugin.
- Starship now identifies shell initialization, Git context, Bash-only Ble.sh support, virtual-environment context, and the absence of a named font requirement.
- AeroSpace already names its exact application/version, macOS platform, Accessibility permission, target paths, installation source, and CLI validation; its reference has no font, theme, plugin, or third-party command dependency.

The clean portable scenario remains clean: a dependency-free capability or a bundled resource needs an explicit “no separate install” explanation, not an invented package. Installation remains a separately confirmed action in every scenario.
