# Reusable rule: interactive preferences stay behind this guard so scripts and
# non-interactive shells do not inherit presentation-only behavior.
if status is-interactive
    # Maintainer Preference: replace Fish's default Emacs-style bindings with
    # vi-style modal editing. This resets existing bindings; users with custom
    # keys should keep them in fish_user_key_bindings instead.
    # Official behavior: https://fishshell.com/docs/current/interactive.html#vi-mode-commands
    fish_vi_key_bindings
end
