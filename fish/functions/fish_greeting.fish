function fish_greeting --description "Show the current time and host"
    # Maintainer Preference: a small dynamic greeting; it contains no fixed host.
    echo The time is (set_color yellow)(date +%T)(set_color normal) and this machine is called (set_color blue)$hostname(set_color normal)
end
