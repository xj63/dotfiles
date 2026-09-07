function ll --description "Long directory listing"
    # Maintainer Preference: preserve the selected `ls` implementation and add
    # long output. Conflicts with an existing function or executable named `ll`.
    ls -l $argv
end
