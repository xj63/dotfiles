function uvr --wraps='uv run python -m' --description "Run a Python module with uv"
    # Maintainer Preference: shorten uv-managed module execution. `uv run` may
    # resolve or create an environment, so the shorthand is not a validation step.
    uv run python -m $argv
end
