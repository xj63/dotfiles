local wezterm = require("wezterm")
local config = wezterm.config_builder()

-- Reusable rule: keep platform-only window effects behind a target check.
local target = wezterm.target_triple
local platform = target:find("windows") and "windows"
  or target:find("apple") and "macos"
  or target:find("linux") and "linux"
  or "unknown"

-- Maintainer Preferences: a dark built-in palette, a distraction-free single
-- pane surface, and a large coding font. Keep a fallback for machines without
-- Monaspace Neon Frozen.
config.color_scheme = "Catppuccin Mocha"
config.enable_tab_bar = false
config.font = wezterm.font_with_fallback({ "Monaspace Neon Frozen", "Menlo" })
config.font_size = 14

if platform == "macos" then
  -- macOS-only preference: native resize border with translucent blurred content.
  config.window_decorations = "RESIZE"
  config.window_background_opacity = 0.8
  config.macos_window_background_blur = 50
elseif platform == "linux" then
  -- Linux/KDE preference: subtle transparency and compositor-provided blur.
  -- Omit blur on other desktops or when it reduces readability/performance.
  config.window_background_opacity = 0.95
  config.kde_window_background_blur = true
elseif platform == "windows" then
  -- Windows preference: request the system tabbed backdrop when supported.
  -- Remove it when the OS or graphics environment renders it poorly.
  config.win32_system_backdrop = "Tabbed"
end

return config
