function py --wraps=python3 --description "Short Python 3 command"
    # Maintainer Preference: make `py` explicitly target Python 3. Preserve an
    # existing launcher named `py`; this wrapper does not install Python.
    python3 $argv
end
