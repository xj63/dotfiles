function ... --wraps='cd ../..' --description "Move up two directories"
    # Maintainer Preference: concise navigation. Fish functions are autoloaded by
    # filename, so the four-dot filename intentionally defines the three-dot name.
    cd ../.. $argv
end
