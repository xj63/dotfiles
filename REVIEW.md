# Review Policy

This policy is the single source of truth for deterministic checks, active Configuration Audits, and pull-request AI review. A clean review has no Blocking Findings. Advisory Findings remain visible until a maintainer records why they are accepted.

## Review scope

- **Staged check**: inspect the exact Git index content about to become a commit.
- **Full deterministic check**: inspect tracked and untracked, non-ignored repository content.
- **Pull-request AI review**: after deterministic CI passes, inspect only the tracked diff, this policy, and the minimum module context needed to judge that diff.

Local Consumer State, Consumer Configurations, backups, ignored files, unrelated filesystem content, and user environment data stay outside every review input.

## Deterministic Blocking Findings

| Rule | Blocking condition | Required remediation |
| --- | --- | --- |
| `secret.github-token` | A GitHub token-shaped value appears in repository content. | Remove it and rotate the credential. |
| `secret.private-key` | Private key material appears in repository content. | Remove it and rotate the key. |
| `secret.hardcoded-credential` | A password, token, secret, or key is assigned a literal credential-like value. | Read it from the environment or use a documented placeholder. |
| `privacy.home-path` | A real macOS or Linux home path identifies a local username. | Use a portable variable or placeholder. |
| `privacy.email` | An email uses a non-example domain without an approved Public Identity Exception. | Use a reserved example address or add a justified exception. |
| `privacy.private-network` | An RFC 1918 address appears in public configuration. | Replace it with a documented example address or placeholder. |
| `privacy.private-host` | A host setting or URL exposes a private `.internal`, `.lan`, or `.local` hostname. | Replace it with a documented placeholder. |
| `privacy.device-identifier` | A MAC-address-shaped device identifier appears in public configuration. | Remove it or use a placeholder. |
| `policy.identity-allowlist` | A Public Identity Exception lacks an exact value or reviewable reason. | Make the exception narrow and explain why it is public. |
| `policy.local-consumer-state` | Content under the Local Consumer State boundary becomes tracked. | Remove it from Git and keep it ignored. |
| `policy.tracked-backup` | A recognized backup path becomes tracked. Its contents are not read by the audit. | Remove it from Git and keep backups outside the repository or ignored. |
| `syntax.json` | A JSON Reference Configuration cannot be parsed. | Correct the syntax before publishing it. |

These rules are a high-confidence floor, not proof that content is safe. Semantic review covers contextual cases that patterns cannot decide.

## Public Identity Exceptions

Public identity exceptions live in the repository allowlist. Each non-comment line contains the exact public value, followed by a tab and a reason. Exceptions apply only to privacy identity rules; they never suppress secret findings.

An exception is appropriate only when the identity is intentionally public and its presence helps the configuration user. Prefer placeholders otherwise.

## Semantic review rules

AI review produces a finding only when it can cite affected diff content and explain the consequence.

### Blocking

- a secret or private identifier not caught deterministically;
- a configuration value that exposes a private service, device, filesystem location, or person;
- an exception that would publish sensitive information rather than an intentional public identity.

### Advisory

- a Maintainer Preference presented as a Reusable Rule;
- platform, application-version, prerequisite, target-location, conflict, or validation context missing when the change needs it;
- an absolute or environment-specific assumption that makes the Reference Configuration misleading;
- a user-affecting configuration, dependency, or protocol change without Upstream Change Information;
- a module explanation that is technically present but not useful to a human reader or consumer AI.

Advisories are remediable or explicitly acceptable rather than unconditional merge blockers. A maintainer who accepts one records a concrete reason in the pull request so later agents can distinguish a decision from an omission.

An unacknowledged Advisory Finding keeps the semantic status check failing. A maintainer may remediate it, or add one line to the pull-request description in the form `AI Review Advisory Reason: <concrete reason>`. Editing the description reruns the checks. The author must have the repository association `OWNER`, `MEMBER`, or `COLLABORATOR`; a reason never overrides a Blocking Finding.

## Finding format

Deterministic findings use this stable shape:

```text
BLOCKING [rule-id] path:line actionable explanation
```

AI findings additionally include severity, evidence from the diff, consequence, and required remediation or maintainer decision.

The semantic review contract is versioned independently of any provider. Each finding contains exactly:

- `severity`: `blocking` or `advisory`;
- `path` and an optional `line` identifying affected repository content;
- `evidence` quoted or precisely paraphrased from the reviewed content;
- `policy_rule` naming the applicable policy concern;
- `consequence` explaining the user or publication impact;
- `disposition` stating the required remediation or maintainer decision.

`scripts/ai-review` is the stable entry point. It runs the deterministic audit before invoking a provider. Pull-request mode constructs its input from Git objects: the tracked diff, this policy at the reviewed commit, and only the README of each affected Application Module. Active-audit mode reads current tracked repository files without following symbolic links. Both modes exclude Local Consumer State and recognized backup paths.

The default provider uses the OpenAI Responses API with response storage disabled and a strict output schema. `AI_REVIEW_COMMAND` may replace it with a command that accepts the versioned review request as JSON on standard input and returns the review result as JSON on standard output. Provider credentials are environment or CI secrets and never repository content.

After changing a provider, model, prompt, or finding schema, run `scripts/evaluate-ai-review`. It exercises the review contract against versioned fixture diffs for contextual privacy, preference framing, prerequisites, portability, justified scope, and clean content. The evaluator tolerates wording variation but requires the expected severity, affected path, policy category, evidence, and disposition.

## Active audit

Ask the repository agent to **audit the current repository using the Review Policy**. The exact execution sequence is `scripts/check all` followed, only on success, by `scripts/ai-review audit`. The agent reports Blocking and Advisory Findings separately.
