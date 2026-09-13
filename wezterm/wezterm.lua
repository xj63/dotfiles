local wezterm = require("wezterm")

-- Reusable rule: config_builder reports unknown keys instead of silently
-- accepting a typo on supported WezTerm releases.
-- Official behavior: https://wezterm.org/config/lua/wezterm/config_builder.html
local config = wezterm.config_builder()

-- Reusable rule: keep platform-only effects behind WezTerm's documented target
-- triple rather than probing unrelated environment variables.
-- Official behavior: https://wezterm.org/config/lua/wezterm/target_triple.html
local target = wezterm.target_triple
local platform = target:find("windows") and "windows"
  or target:find("apple") and "macos"
  or target:find("linux") and "linux"
  or "unknown"

-- Maintainer Preference: select a non-default built-in Catppuccin palette.
-- Preserve an existing `colors` override because it takes precedence over parts
-- of a named scheme. https://wezterm.org/config/appearance.html
config.color_scheme = "Catppuccin Mocha"

-- Maintainer Preference: hide the tab bar (the default is visible). This hides
-- tab status/navigation, so users with multiple tabs need another control.
-- https://wezterm.org/config/lua/config/enable_tab_bar.html
config.enable_tab_bar = false

-- Maintainer Preference: prefer the exact Monaspace Neon Frozen family from
-- GitHub Next's Monaspace Frozen Fonts package, then fall back to macOS Menlo.
-- Other platforms should substitute an installed fallback. Neither font is
-- installed by this file; inspect resolution with `wezterm ls-fonts`.
-- https://github.com/githubnext/monaspace/releases
-- https://wezterm.org/config/fonts.html
config.font = wezterm.font_with_fallback({ "Monaspace Neon Frozen", "Menlo" })

-- Maintainer Preference: 14pt differs from the 12pt default and trades terminal
-- density for readability. https://wezterm.org/config/lua/config/font_size.html
config.font_size = 14

if platform == "macos" then
  -- macOS preference: remove the title bar but retain resize borders. Combined
  -- with a hidden tab bar, moving the window may require modifier-drag.
  -- https://wezterm.org/config/lua/config/window_decorations.html
  config.window_decorations = "RESIZE"

  -- Maintainer Preference: 80% opacity and strong blur differ from the opaque,
  -- no-blur defaults; transparency can reduce contrast and performance.
  -- https://wezterm.org/config/lua/config/window_background_opacity.html
  -- https://wezterm.org/config/lua/config/macos_window_background_blur.html
  config.window_background_opacity = 0.8
  config.macos_window_background_blur = 50
elseif platform == "linux" then
  -- Linux preference: subtle transparency only. The former KDE blur option is
  -- nightly-only and deprecated, so this stable reference omits it.
  config.window_background_opacity = 0.95
elseif platform == "windows" then
  -- Windows 11 build 22621+ preference: Tabbed requires opacity below 1. Use the
  -- documented 0 value for system material; remove both on unsupported systems.
  -- https://wezterm.org/config/lua/config/win32_system_backdrop.html
  config.window_background_opacity = 0
  config.win32_system_backdrop = "Tabbed"
end

return config
