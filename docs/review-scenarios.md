# Local semantic review scenarios

Use these scenarios when changing `REVIEW.md`, the repository agent protocol, or the local AI used for a Configuration Audit. They are judgment checks, not executable fixtures. Review them only after `scripts/check all` passes.

For each scenario, require the local AI to identify the affected content, cite relevant evidence, apply the Review Policy, explain the consequence, and give a remediation or maintainer disposition.

| Scenario | Synthetic change | Expected result |
| --- | --- | --- |
| Contextual privacy | A terminal reference starts an SSH session to a person-specific bedroom NAS name that deterministic patterns do not recognize. | **Blocking**: the name identifies a private person or device and must become a public placeholder. |
| Preference framed as universal | A shell comment says autosuggestions are always distracting and everyone should disable them. | **Advisory**: label the choice as a Maintainer Preference or explain a reusable condition. |
| Missing prerequisite | A Fish configuration invokes `fzf_configure_bindings`, but the module README does not mention the plugin or installation. | **Advisory**: document the prerequisite, detection method, and appropriate installation guidance. |
| Untraceable visual dependency | An editor selects a named third-party theme and font, but its README says only that extensions and fonts are optional. | **Advisory**: name the exact theme extension and font package, map each to the affected setting, explain how to detect it, and link to first-party acquisition guidance. |
| Portability assumption | An editor configuration hard-codes `/opt/homebrew/bin/fish` without a platform condition or substitution guidance. | **Advisory**: detect the executable or document the scoped assumption and portable substitution. |
| Justified platform scope | A module explicitly says it is tested on macOS with Homebrew, explains why the reference uses that prefix, and tells other users to substitute their detected path. | **No finding**: the limitation and adaptation path are honest and usable. |
| Removed private content | A diff replaces a person-specific private device name with `host.example.com`; the sensitive-looking value appears only on a deleted line. | **No finding**: the change remediates the risk. |
| Clean portable change | A Fish setting uses portable syntax, calls a subjective choice a Maintainer Preference, and includes target and safe-validation guidance. | **No finding**. |

Record the outcome in the pull-request description or a review comment. If an expected category changes, update the Review Policy or document why the scenario is no longer representative in the same pull request.
