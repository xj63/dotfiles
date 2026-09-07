# Reusable rule: interactive preferences stay behind this guard so scripts and
# non-interactive shells do not inherit presentation-only behavior.
if status is-interactive
    # Maintainer Preference: replace Fish's default Emacs-style bindings with
    # vi-style modal editing. This resets existing bindings; users with custom
    # keys should keep them in fish_user_key_bindings instead.
    # Official behavior: https://fishshell.com/docs/current/interactive.html#vi-mode-commands
    fish_vi_key_bindings

    # Maintainer Preference: provide a compact Git status abbreviation only when
    # Git already exists and `gst` does not conflict with a local command.
    if command --query git
        # Abbreviations expand visibly in the editable command line; unlike an
        # alias, the resulting Git command remains inspectable before execution.
        abbr --add gst 'git status --short --branch'
    end
end

# Maintainer Preferences: load optional application integrations only when their
# local files exist. OrbStack supplies its shell integration; LM Studio exposes
# its CLI; Antigravity exposes its bundled command-line tools. Sourcing OrbStack
# may change shell startup behavior, while the two added bin directories can
# take precedence over same-named commands already on PATH.
# File-owned paths use global scope so removing these lines removes their effect
# in the next Fish process instead of leaving universal fish_user_paths state.
# Official behavior: https://fishshell.com/docs/current/cmds/fish_add_path.html
test -f "$HOME/.orbstack/shell/init2.fish"; and source "$HOME/.orbstack/shell/init2.fish" 2>/dev/null
test -d "$HOME/.lmstudio/bin"; and fish_add_path --global "$HOME/.lmstudio/bin"
test -d "$HOME/.antigravity/antigravity/bin"; and fish_add_path --global "$HOME/.antigravity/antigravity/bin"
