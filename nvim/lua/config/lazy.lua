local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"

-- Reusable rule: this follows the official LazyVim starter bootstrap: install
-- only lazy.nvim's stable branch into Neovim's data directory, then stop visibly
-- if cloning fails. First startup performs a network and filesystem mutation.
-- Upstream reference: https://github.com/LazyVim/starter/blob/main/lua/config/lazy.lua
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
    -- Maintainer Preference: follow the LazyVim starter recommendation to use
    -- current Git commits instead of often-stale plugin release tags. The lock
    -- file still pins resolved commits until the user deliberately updates it.
    -- https://lazy.folke.io/spec/versioning
    version = false,
  },
  -- Maintainer Preference: try Catppuccin first during bootstrap and retain
  -- Neovim's built-in habamax as a dependency-free recovery fallback.
  install = { colorscheme = { "catppuccin-mocha", "habamax" } },
  checker = {
    -- Maintainer Preference: check for available updates in the background but
    -- do not interrupt editing with notifications. Disable this for offline or
    -- tightly controlled environments.
    enabled = true,
    notify = false,
  },
  performance = {
    rtp = {
      -- Maintainer Preference: reduce runtime-path work by disabling unused
      -- built-ins. Keep an entry when its lost capability matters:
      -- gzip/tarPlugin/zipPlugin edit compressed archives, tohtml converts the
      -- current buffer to HTML, and tutor provides :Tutor.
      -- https://lazy.folke.io/configuration
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
