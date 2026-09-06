---
status: accepted
---

# Protect main with deterministic and semantic review

All changes reach `main` through pull requests guarded by deterministic checks and AI semantic review. Deterministic checks run first and share one policy with active audits; the AI then receives only the tracked diff and necessary repository context, blocking secret or privacy risks while reporting generality and portability concerns as auditable advice.
