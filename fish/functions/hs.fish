function hs --wraps='wezterm cli split-pane --bottom' --description "Split the current WezTerm pane downward"
    # Maintainer Preference: horizontal WezTerm split shorthand. It requires a
    # live WezTerm mux context and conflicts with any existing `hs` command.
    wezterm cli split-pane --bottom $argv
end
