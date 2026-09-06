# Repository architecture

## Purpose

This repository is an AI-first Configuration Knowledge Base. It gives a user's AI enough context to understand, select, and adapt sanitized Reference Configurations while preserving the user's ownership, intent, and recovery path.

It is not a dotfile installer, a home-directory mirror, or a synchronization service. A Consumer Configuration remains independent from this repository.

## Planned repository shape

```text
/
├── README.md
├── AGENTS.md
├── CONTEXT.md
├── CHANGELOG.md
├── REVIEW.md
├── .gitignore
├── .githooks/
│   └── pre-commit
├── scripts/
│   ├── check
│   └── install-hooks
├── .github/workflows/
│   └── checks.yml
├── docs/
│   ├── adr/
│   └── agents/
├── fish/
│   ├── README.md
│   ├── config.fish
│   └── conf.d/
├── zed/
│   ├── README.md
│   ├── settings.json
│   └── keymap.json
└── wezterm/
    ├── README.md
    └── wezterm.lua
```

Application Modules live directly at the repository root. Repository infrastructure uses conventional root files, `docs/`, `scripts/`, and `.github/`; there is no `apps/` wrapper.

## Application Module contract

Each Application Module contains one coherent Reference Configuration and a human-readable `README.md`. Files are organized relative to the application's native configuration root rather than the user's home directory. The README states the actual target location.

Configuration comments are the primary location for explaining capabilities, applicable conditions, conflicts, and Maintainer Preferences. When the native format cannot safely carry comments, the module README carries that explanation. Mutually exclusive alternatives are explained in comments first and become separate files only when a single coherent reference cannot express them.

A module README uses only the sections that add information. Its available subjects are:

- purpose;
- applicable environments;
- prerequisites and installation guidance;
- target configuration location;
- included capabilities;
- Maintainer Preferences;
- known conflicts;
- safe validation.

The prose remains natural and human-readable. The repository does not require a machine-readable module manifest. English is normative; a Chinese entry point or translation may be supplied without becoming a second source of truth.

## Consumer-AI entry points

The root `README.md` explains the project to a person and supplies a prompt they can copy into an AI tool. Root `AGENTS.md` holds the executable repository protocol for tools that load agent instructions automatically. Each module README supplies application-local knowledge.

When asked to configure an application, the user's AI follows this sequence:

1. Understand the user's goal and unresolved choices.
2. Inspect the existing Consumer Configuration, environment, application version, and available dependencies.
3. Read the relevant Application Module and only the repository guidance it points to.
4. Present the proposed changes, effects, conflicts, dependencies, and validation plan.
5. Obtain confirmation before behavior changes, overwrites, dependency installation, application restarts, or other consequential actions.
6. Establish a Recovery Path, then make the smallest changes that satisfy the accepted intent.
7. Run safe, read-only or side-effect-free validation described by the module. Stop on failure and offer the Recovery Path.
8. Update the User Intent Record and Review Cursor.

Missing applications or dependencies are detected and explained automatically. Installation uses an official source or a package manager chosen by the user, and begins only after explicit confirmation.

## User intent and local privacy

The User Intent Record stores current goals and reasons rather than an append-only activity log. Its location follows this priority:

1. comments in the Consumer Configuration when the format supports them;
2. a Markdown document inside the user's application configuration directory when the configuration is directory-based;
3. ignored `.local/` state inside the cloned knowledge base when intent cannot live beside the Consumer Configuration.

The same record stores the last reviewed release or commit as a Review Cursor. A Review Cursor is input to change assessment; it never authorizes synchronization.

`.local/` contains neither configuration copies nor credentials and never enters Git, audits, AI review context, or backups committed to this repository.

## Upstream update protocol

Every user-affecting configuration, dependency, or protocol change updates the `[Unreleased]` section of `CHANGELOG.md` in the same pull request. Each entry identifies the affected application, classifies the change, explains user impact, and supplies migration guidance when relevant.

The repository uses Semantic Versioning. Breaking repository protocols or module layouts increment the major version; new modules, capabilities, dependencies, or behavior increment the minor version; documentation and non-behavioral corrections increment the patch version. Releases may batch entries from `[Unreleased]` into Git tags and GitHub Releases.

After pulling upstream, a user's AI reads changes after the Review Cursor, filters them to relevant Application Modules, and inspects the corresponding diff. It produces an impact report before editing. Behavior, dependency, and preference changes require user approval.

`scripts/update-context <Review-Cursor> <application>` is the read-only seam for this assessment. It emits only newly added change information for the selected Application Module and the relevant tracked diff through the reviewed target commit, including shared consumer-protocol files. It receives no Consumer Configuration path and performs no synchronization.

## Review architecture

`REVIEW.md` is the single source of truth for deterministic checks, active Configuration Audits, and pull-request AI review. `AGENTS.md` exposes a direct instruction for invoking a full audit.

The review pipeline is ordered:

1. `scripts/check` runs deterministic secret, privacy-pattern, path, syntax, and repository-policy checks.
2. pre-commit invokes that same entry point against the staged change.
3. CI invokes the same entry point as a required pull-request check.
4. Before creating or updating a pull request, the maintainer's local AI reviews the tracked diff, `REVIEW.md`, and the minimum necessary module context.
5. Blocking Findings are remediated before merge. Advisory Findings are recorded in the pull request and may be accepted with a maintainer reason.

The AI review context excludes `.local/`, Consumer Configurations, backups, unrelated filesystem content, and user environment data. Public identity is accepted only through an explicit allowlist.

Semantic review uses the maintainer's existing local AI session and requires no repository AI credential. GitHub CI remains deterministic, reproducible, and free of provider coupling.

## Branch and release contract

All changes reach `main` through pull requests. Branch protection requires the deterministic check; the local semantic audit is a maintainer workflow recorded in the pull request. `main` remains readable and usable by a consumer AI, while GitHub Releases mark versioned review checkpoints.

## Implementation sequence

1. Add the human and AI entry points, review policy, ignored local-state boundary, CHANGELOG, deterministic check entry point, and required workflows.
2. Implement one Application Module end to end as a tracer of authoring, consumer guidance, validation, review, and update behavior.
3. Refine the contracts from that tracer, then add further Application Modules without introducing cross-module coupling.
