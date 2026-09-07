local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"

-- Reusable rule: bootstrap only the stable lazy.nvim branch and stop visibly if
-- cloning fails. First startup performs a network and filesystem mutation.
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local repository = "https://github.com/folke/lazy.nvim.git"
  local output = vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", repository, lazypath })
  if vim.v.shell_error ~= 0 then
    vim.api.nvim_echo({
      { "Failed to clone lazy.nvim:\n", "ErrorMsg" },
      { output, "WarningMsg" },
      { "\nPress any key to exit...", "MoreMsg" },
    }, true, {})
    vim.fn.getchar()
    os.exit(1)
  end
end

vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  spec = {
    { "LazyVim/LazyVim", import = "lazyvim.plugins" },
    { import = "plugins" },
  },
  defaults = {
    -- Maintainer Preference: use exact commits from lazy-lock.json rather than
    -- plugin release tags; update the lock file deliberately.
    lazy = false,
    version = false,
  },
  install = { colorscheme = { "catppuccin-mocha", "habamax" } },
  checker = {
    enabled = true,
    notify = false,
  },
  performance = {
    rtp = {
      disabled_plugins = {
        "gzip",
        "tarPlugin",
        "tohtml",
        "tutor",
        "zipPlugin",
      },
    },
  },
})
