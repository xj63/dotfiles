function ls --wraps=ls --description "Use eza when available, otherwise system ls"
    if command --query eza
        eza --icons auto --git $argv
    else
        command ls $argv
    end
end
