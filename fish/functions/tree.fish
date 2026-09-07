function tree --description "Tree view through eza"
    # Maintainer Preference: use Eza's tree rendering instead of another `tree`
    # program. Fail with a clear diagnostic rather than installing Eza.
    command --query eza; or begin
        echo "tree requires eza" >&2
        return 127
    end
    eza --tree $argv
end
