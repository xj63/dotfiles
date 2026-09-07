# AI-first configuration knowledge base

This repository contains sanitized Reference Configurations and the knowledge needed for an AI to adapt them to a person's existing setup. It is not an installer, a home-directory mirror, or a promise that any configuration should be copied unchanged.

Choose only the Application Module you need. Each root-level module explains its own supported environment, prerequisites, target location, capabilities, subjective Maintainer Preferences, conflicts, and safe validation. Your configuration remains yours and is never synchronized with this repository.

## Copyable prompt

Replace the bracketed text, then give this prompt to an AI that can read this clone and your configuration files:

```text
Help me configure [application] using this repository as a Configuration Knowledge Base.

Read AGENTS.md, REVIEW.md, and the relevant application README before proposing changes. First understand my goal and inspect my existing configuration, application version, operating system, and available dependencies. Do not copy the reference unchanged and do not modify anything yet.

Present the smallest plan that satisfies my goal. Explain behavior changes, prerequisites, conflicts, Maintainer Preferences, validation, and the recovery path. Ask for confirmation before changing behavior, overwriting files, installing anything, or restarting an application. After confirmation, preserve unrelated settings, make the agreed change, and run only safe validation. On failure, stop, show the diagnostic, and ask before applying the recovery path. On success, save my current goal, reasons, and the reviewed upstream release or commit beside my configuration when possible.

I want help with: [goal]
```

Available Application Modules are [AeroSpace](aerospace/README.md), [Fish](fish/README.md), [Neovim](nvim/README.md), [Starship](starship/README.md), [WezTerm](wezterm/README.md), and [Zed](zed/README.md). Select only the module relevant to the current goal; users and AI tools do not need to inspect the others.

## Reviewing newer Fish guidance

Use this prompt after pulling a newer version of this repository:

```text
Review Fish changes after the Review Cursor in my current intent record. Follow AGENTS.md and fish/README.md, generate the Fish-only update context, and compare it with my current configuration and goals. Give me an impact report before proposing edits. Ask before behavior, dependency, or preference changes; if I decline, leave my configuration and cursor unchanged. If I accept selected changes, establish recovery, apply only those changes, validate, update my current intent, and advance the cursor to the reviewed upstream state.
```

## Repository maintenance

Repository changes follow [AGENTS.md](AGENTS.md) and the shared [Review Policy](REVIEW.md). Known secret and privacy patterns are checked locally at commit time and again in GitHub Actions. Semantic Configuration Audits run in the maintainer's existing local AI session and are recorded in the pull request.

Contributor AIs add independent root-level modules using the natural-language [Application Module authoring guide](docs/application-modules.md). No module manifest is required.
