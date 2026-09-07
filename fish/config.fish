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
