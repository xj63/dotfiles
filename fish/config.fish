# Reusable rule: interactive preferences stay behind this guard so scripts and
# non-interactive shells do not inherit presentation-only behavior.
if status is-interactive
    # Maintainer Preference: use vi-style editing. Keep Fish's default bindings
    # when modal editing is unfamiliar or conflicts with existing key mappings.
    fish_vi_key_bindings

    # Maintainer Preference: provide a compact Git status abbreviation only when
    # Git already exists and `gst` does not conflict with a local command.
    if command --query git
        abbr --add --global gst 'git status --short --branch'
    end
end

# Optional application integrations are loaded only when their local files exist.
test -f "$HOME/.orbstack/shell/init2.fish"; and source "$HOME/.orbstack/shell/init2.fish" 2>/dev/null
test -d "$HOME/.lmstudio/bin"; and fish_add_path "$HOME/.lmstudio/bin"
test -d "$HOME/.antigravity/antigravity/bin"; and fish_add_path "$HOME/.antigravity/antigravity/bin"
