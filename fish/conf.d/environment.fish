# Reusable rule: add optional toolchains only when their installation exists.
if test -x /opt/homebrew/bin/brew
    # Maintainer Preference: import Homebrew's Apple Silicon environment before
    # other optional toolchains. It can shadow system commands through PATH.
    /opt/homebrew/bin/brew shellenv | source
    # Maintainer Preference: suppress Homebrew environment hint messages.
    set --global --export HOMEBREW_NO_ENV_HINTS 1
end

if command --query nvim
    # Maintainer Preference: use Neovim for both interactive and tool-invoked
    # editing. Preserve an existing editor choice unless the user selects this.
    set --global --export EDITOR nvim
    set --global --export VISUAL nvim
end

if test -f "$HOME/.cargo/env.fish"
    # Reusable Rule for an optional Rustup capability: source its
    # installation-owned environment instead of copying generated contents.
    # Choosing Rustup itself is a Maintainer Preference and may conflict with
    # another Rust toolchain manager that also controls PATH.
    source "$HOME/.cargo/env.fish"
end

# Maintainer Preference: use the standard macOS Android Studio SDK location.
# This exports Android's legacy and current environment names and prepends its
# emulator/platform tools, which can override another SDK manager's commands.
# Reusable Rule: avoid pinning a local NDK or Build Tools version; Android
# projects should select those versions themselves.
if test -d "$HOME/Library/Android/sdk"
    set --global --export ANDROID_SDK_ROOT "$HOME/Library/Android/sdk"
    set --global --export ANDROID_HOME "$ANDROID_SDK_ROOT"
    # Prepending can shadow other Android tools. Use global scope so the file,
    # rather than persistent universal state, owns this PATH decision.
    fish_add_path --global "$ANDROID_SDK_ROOT/emulator" "$ANDROID_SDK_ROOT/platform-tools"
end

if test -d "/Applications/Android Studio.app/Contents/jbr/Contents/Home"
    # Maintainer Preference: use Android Studio's bundled JBR as the global Java
    # runtime so Android tooling follows the IDE. This can override a JDK chosen
    # by a project manager such as SDKMAN!, jenv, asdf, or mise; omit this block
    # when a project or toolchain must control JAVA_HOME.
    set --global --export JAVA_HOME "/Applications/Android Studio.app/Contents/jbr/Contents/Home"
    fish_add_path --global "$JAVA_HOME/bin"
end
