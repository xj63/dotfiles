function imgcat --wraps='wezterm imgcat' --description "Render an image through WezTerm"
    # Maintainer Preference: route inline image display through WezTerm. Output is
    # terminal-specific and may be unsuitable when redirected or used over SSH.
    wezterm imgcat $argv
end
