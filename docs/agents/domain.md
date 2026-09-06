# Domain docs

This repository uses a single-context domain-documentation layout.

## Before exploring

- Read `CONTEXT.md` at the repository root when it exists.
- Read ADRs under `docs/adr/` that affect the area being changed.
- If either path does not exist, proceed silently. Domain-modeling flows create them lazily when terminology or decisions are resolved.

## Use the glossary's vocabulary

Use canonical terms from `CONTEXT.md` in issue titles, specifications, tests, documentation, and code. Do not drift to synonyms that the glossary explicitly avoids.

If a needed concept is missing, reconsider whether it belongs to the domain vocabulary or note the gap for domain modeling.

## Flag ADR conflicts

If proposed work contradicts an existing ADR, identify the conflict explicitly instead of silently overriding the decision.
