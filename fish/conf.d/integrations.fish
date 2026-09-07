# Reusable rule: conf.d runs for non-interactive shells too, so prompt and key
# integrations must be both interactive-only and conditional on the executable.
# Official startup order: https://fishshell.com/docs/current/language.html#configuration-files
if status is-interactive
    # Maintainer Preferences: FZF key bindings, Starship prompt rendering, and
    # Zoxide directory jumping. Each command emits Fish code and can conflict
    # with existing bindings, prompts, or directory functions.
    command --query fzf; and fzf --fish | source
    command --query starship; and starship init fish | source
    command --query zoxide; and zoxide init fish | source
end
