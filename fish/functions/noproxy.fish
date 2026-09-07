function noproxy --description "Clear common proxy variables for this shell"
    # Maintainer Preference: explicitly opt the current shell and descendants out
    # of common proxy conventions. This can break proxy-dependent network access.
    set --erase HTTP_PROXY HTTPS_PROXY ALL_PROXY
    set --erase http_proxy https_proxy all_proxy
end
