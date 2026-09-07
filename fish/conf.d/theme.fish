# Maintainer Preference: pin the maintainer's Nord-derived interactive palette.
# It began as Fish 4.9.2's bundled Nord theme, then deliberately uses a bright
# match background and lighter prefix/normal styling. Remove this file when
# fish_config or another theme owns the same variables.
# Upstream source: https://github.com/fish-shell/fish-shell/blob/4.9.2/share/themes/nord.theme
# Variable meanings: https://fishshell.com/docs/current/interactive.html#syntax-highlighting-variables
if status is-interactive
    set --global fish_color_autosuggestion 4c566a
    set --global fish_color_cancel --reverse
    set --global fish_color_command 88c0d0
    set --global fish_color_comment 4c566a --italics
    set --global fish_color_cwd 5e81ac
    set --global fish_color_cwd_root bf616a
    set --global fish_color_end 81a1c1
    set --global fish_color_error bf616a
    set --global fish_color_escape ebcb8b
    set --global fish_color_history_current e5e9f0 --bold
    set --global fish_color_host a3be8c
    set --global fish_color_host_remote ebcb8b
    set --global fish_color_keyword 81a1c1
    set --global fish_color_match --background=brblue
    set --global fish_color_normal normal
    set --global fish_color_operator 81a1c1
    set --global fish_color_option 8fbcbb
    set --global fish_color_param d8dee9
    set --global fish_color_quote a3be8c
    set --global fish_color_redirection b48ead --bold
    set --global fish_color_search_match --bold --background=434c5e
    set --global fish_color_selection d8dee9 --bold --background=434c5e
    set --global fish_color_status bf616a
    set --global fish_color_user a3be8c
    set --global fish_color_valid_path --underline
    set --global fish_pager_color_completion e5e9f0
    set --global fish_pager_color_description ebcb8b --italics
    set --global fish_pager_color_prefix normal --bold --underline
    set --global fish_pager_color_progress 3b4252 --background=d08770
    set --global fish_pager_color_selected_background --background=434c5e
end
