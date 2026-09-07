function tree --description "Tree view through eza"
    command --query eza; or begin
        echo "tree requires eza" >&2
        return 127
    end
    eza --tree $argv
end
