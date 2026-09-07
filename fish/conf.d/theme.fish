# Maintainer Preference: use Fish's bundled Nord theme for interactive shells.
# Loading the named theme avoids copying Fish-generated color variables into
# this repository and lets the palette follow the installed Fish version.
# This overrides another theme chosen earlier in startup; remove this file when
# the user wants Fish's default or another theme.
# Official behavior: https://fishshell.com/docs/current/cmds/fish_config.html
if status is-interactive
    fish_config theme choose Nord
end
