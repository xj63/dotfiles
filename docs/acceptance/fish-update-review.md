# Fish upstream-update acceptance

Date: 2026-09-07

The maintainer's local AI exercised the update protocol against temporary upstream histories and Consumer Configurations. The scenarios used a baseline commit as the Review Cursor, later Fish behavior and Maintainer Preference entries, an irrelevant WezTerm entry, and corresponding tracked changes.

## Focused impact context

- `scripts/update-context <cursor> fish` reported the resolved `From` and `To` commits.
- The output included both Fish entries and the Fish diff while excluding the WezTerm entry and configuration diff.
- A Fish file change without added Fish change information stopped with an actionable diagnostic.
- Generating the context received no Consumer Configuration path and left an external configuration plus its intent file byte-for-byte unchanged.

## Declined update

The read-only scenario represents a user declining the proposed behavior: the Consumer Configuration hashes did not change and the intent record retained its earlier Review Cursor.

## Partial acceptance

The impact report presented the quiet greeting as a behavior change and `gst` as a Maintainer Preference. The scripted user decision accepted the quiet greeting and declined `gst`.

- The AI preserved the unrelated `EDITOR` setting and added only the accepted interactive greeting behavior.
- The resulting Consumer Configuration contained no `gst` abbreviation.
- `fish --no-config --no-execute` returned exit status 0.
- The current intent recorded the goal, the reason for declining `gst`, and the reviewed `To` commit as the new Review Cursor.

Advancing the cursor recorded review of the whole upstream range; it did not claim that every upstream preference was adopted.
