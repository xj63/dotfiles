function fish_greeting --description "Show the current time and host"
    # Maintainer Preference: replace Fish's standard greeting with time and the
    # runtime hostname. No host is stored here, but showing it on screen may be
    # undesirable during demos or screen sharing.
    # Official hook: https://fishshell.com/docs/current/interactive.html#configurable-greeting
    echo The time is (set_color yellow)(date +%T)(set_color normal) and this machine is called (set_color blue)$hostname(set_color normal)
end
