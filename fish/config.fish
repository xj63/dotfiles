# Reusable rule: interactive preferences belong behind this guard so scripts and
# non-interactive Fish processes do not inherit presentation-only behavior.
if status is-interactive
    # Maintainer Preference: start the interactive shell without Fish's greeting.
    # Keep the default greeting when the user values discoverability for new shells.
    set --global fish_greeting

    # Maintainer Preference: provide one memorable shortcut when Git is available.
    # Do not install Git for this abbreviation; omit it when the user has another
    # `gst` abbreviation or prefers to type the full command.
    if command --query git
        abbr --add --global gst 'git status --short --branch'
    end
end
