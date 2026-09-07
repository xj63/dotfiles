function uvr --wraps='uv run python -m' --description "Run a Python module with uv"
    uv run python -m $argv
end
