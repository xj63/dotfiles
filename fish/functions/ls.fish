function ls --wraps=ls --description "Use eza when available, otherwise system ls"
    # Maintainer Preference: enrich the core listing with icons and Git state.
    # This name replaces `ls`; fall back to the system command when Eza is absent.
    if command --query eza
        eza --icons auto --git $argv
    else
        command ls $argv
    end
end
