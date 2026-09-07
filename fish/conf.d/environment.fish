# Reusable rule: add optional toolchains only when their installation exists.
if test -x /opt/homebrew/bin/brew
    /opt/homebrew/bin/brew shellenv | source
    # Maintainer Preference: suppress Homebrew environment hint messages.
    set --global --export HOMEBREW_NO_ENV_HINTS 1
end

if command --query nvim
    set --global --export EDITOR nvim
    set --global --export VISUAL nvim
end

if test -f "$HOME/.cargo/env.fish"
    source "$HOME/.cargo/env.fish"
end

# Optional macOS Android Studio layout. Avoid pinning a local NDK or Build Tools
# version; Android projects should select those versions themselves.
if test -d "$HOME/Library/Android/sdk"
    set --global --export ANDROID_SDK_ROOT "$HOME/Library/Android/sdk"
    set --global --export ANDROID_HOME "$ANDROID_SDK_ROOT"
    fish_add_path "$ANDROID_SDK_ROOT/emulator" "$ANDROID_SDK_ROOT/platform-tools"
end

if test -d "/Applications/Android Studio.app/Contents/jbr/Contents/Home"
    set --global --export JAVA_HOME "/Applications/Android Studio.app/Contents/jbr/Contents/Home"
    fish_add_path "$JAVA_HOME/bin"
end
