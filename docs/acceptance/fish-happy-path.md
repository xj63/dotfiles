# Fish consumer-guidance acceptance record

Date: 2026-09-07

This is a historical acceptance record for the Fish reference at that date, not a description of the current module. Later changes removed the quiet greeting and `gst` abbreviation used by these fixtures; the scenarios remain evidence for sequencing, confirmation, recovery, validation, and intent preservation.

This provider-free acceptance run used the repository's current local AI session and three isolated temporary Consumer Configurations. The AI read the root prompt, `AGENTS.md`, `REVIEW.md`, `fish/README.md`, and `fish/config.fish` before acting. Temporary files were outside the repository and contained no credentials or real user data.

## Missing dependency and declined action

The controlled environment had an empty `PATH`, so `command -v fish` returned no result. The existing Consumer Configuration contained only an unrelated `EDITOR` setting.

The AI first reported that Fish was required, pointed to the official installation source, and proposed installation as a separate consequential action before any configuration edit. The scripted user response declined installation. The AI stopped without installing Fish or editing the file. Its SHA-256 remained `7507eaff0f1096cbe382cad82bf0b56c8665e2939828e00900176be5e5921529` before and after the response.

## Accepted happy path

The controlled environment provided Fish 4.9.2. Inspection found the existing `EDITOR` setting and no conflicting Fish greeting or `gst` definition. Before modification, the AI proposed adding the quiet greeting and conditional Git abbreviation, explained both as Maintainer Preferences, described syntax validation, and received the scripted user's acceptance.

The AI merged only those capabilities. The unrelated `set --global --export EDITOR vi` line remained present. `fish --no-config --no-execute` returned exit status 0 against the resulting file. The AI then created the user-approved companion intent record containing the current goal, reasons, and Review Cursor `3e5de9d71936bcd2555c9b5d619619520a97e954`. That commit contains `fish/config.fish`, and a later-session read recovered all three intent fields and resolved the reviewed Fish snapshot from the cursor.

## Validation failure stop

A third isolated candidate deliberately omitted the closing `end` for an interactive guard. Fish returned exit status 127 with a missing-`end` diagnostic. The AI stopped at validation, did not create a success intent record, and left restoration as a separately confirmed action.

## Result

The acceptance run demonstrated inspection before planning, a plan before modification, confirmation boundaries for dependency installation and behavior changes, an unchanged declined fixture, preservation of unrelated settings, observable success and failure validation, stop-on-failure behavior, and intent plus Review Cursor survival for a later AI session.
