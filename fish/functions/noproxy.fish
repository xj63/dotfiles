function noproxy --description "Clear common proxy variables for this shell"
    set --erase HTTP_PROXY HTTPS_PROXY ALL_PROXY
    set --erase http_proxy https_proxy all_proxy
end
