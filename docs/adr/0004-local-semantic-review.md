---
status: accepted
supersedes: 0003-two-layer-pull-request-gate.md
---

# Keep semantic review local

Semantic Configuration Audits run in the maintainer's existing local AI session before a pull request is created or updated. The audit follows `REVIEW.md`, begins with the deterministic repository check, reviews only tracked diff and necessary module context, and records Blocking and Advisory Findings in the pull request.

GitHub does not invoke an AI provider and stores no AI credential for this repository. Branch protection requires the deterministic status check and pull-request workflow. This keeps hosted CI reproducible and avoids provider credentials or usage costs while retaining semantic review as an explicit maintainer protocol.
