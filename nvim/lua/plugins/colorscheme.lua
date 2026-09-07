return {
  {
    "catppuccin/nvim",
    -- Maintainer Preference: register the plugin under the name expected by the
    -- lock file and load it before other UI plugins to avoid startup flashes.
    name = "catppuccin",
    priority = 1000,
    opts = {
      -- Maintainer Preference: differs from Catppuccin's false default. Let the
      -- terminal/GUI show through; floating windows may lose visual separation.
      -- https://github.com/catppuccin/nvim#configuration
      transparent_background = true,
    },
  },
  {
    "LazyVim/LazyVim",
    opts = {
      -- Maintainer Preference: replace LazyVim's default Tokyonight scheme.
      colorscheme = "catppuccin-mocha",
    },
  },
}
