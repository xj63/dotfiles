function vs --wraps='wezterm cli split-pane --right' --description "Split the current WezTerm pane rightward"
    # Maintainer Preference: vertical WezTerm split shorthand. It requires a live
    # WezTerm mux context and conflicts with any existing `vs` command.
    wezterm cli split-pane --right $argv
end
