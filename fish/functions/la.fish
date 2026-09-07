function la --description "Long directory listing including hidden entries"
    # Maintainer Preference: compose `ll` with hidden entries. This inherits any
    # behavior or conflict introduced by the local `ll` and `ls` functions.
    ll -a $argv
end
