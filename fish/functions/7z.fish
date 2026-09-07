function 7z --wraps=7zz --description "Use the 7-Zip 7zz executable"
    # Maintainer Preference: retain the familiar `7z` spelling when the installed
    # 7-Zip package exposes `7zz`. Invocation fails normally when it is absent.
    7zz $argv
end
