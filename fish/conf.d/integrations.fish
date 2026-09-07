# Reusable rule: shell integrations are optional and must not make Fish startup
# fail when a tool is absent.
command --query fzf; and fzf --fish | source
command --query starship; and starship init fish | source
command --query zoxide; and zoxide init fish | source
