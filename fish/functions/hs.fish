function hs --wraps='wezterm cli split-pane --bottom' --description "Split the current WezTerm pane downward"
    wezterm cli split-pane --bottom $argv
end
