# AI-first configuration knowledge base

This repository provides application-scoped configuration knowledge that an AI can interpret, select, and adapt for a user. Reference files demonstrate coherent configurations; they are not universal files to copy unchanged.

## Language

**Configuration Knowledge Base**:
A collection of configuration knowledge that an AI reads, selects, and adapts while helping a user create or maintain their own configuration.
_Avoid_: Configuration installer, universal dotfiles

**Application Module**:
An independent knowledge unit for one application. It declares its own applicable environment and prerequisites instead of inheriting a repository-wide platform promise.
_Avoid_: Configuration package, plugin

**Reference Configuration**:
A sanitized, coherent, working example that demonstrates one implementation without claiming every user should adopt it unchanged.
_Avoid_: Standard configuration, default configuration

**Reusable Rule**:
Configuration knowledge that an AI may select for a user without inheriting a maintainer-specific preference.
_Avoid_: Best practice

**Maintainer Preference**:
A subjective choice embodied by a Reference Configuration. An AI presents it as a choice rather than a universal rule.
_Avoid_: Recommended setting

**Consumer Configuration**:
A configuration owned and maintained by a user, with or without version control. It has no synchronization relationship with this repository.
_Avoid_: Generated copy, managed configuration

**User Intent Record**:
The user's current configuration goals and reasons, maintained by their AI. It lives in configuration comments first, a document inside the user's application configuration directory second, and ignored clone-local state only as a fallback.
_Avoid_: Upstream content, operation log

**Local Consumer State**:
Optional private context in an ignored directory of a repository clone, used only when a User Intent Record cannot live beside the Consumer Configuration.
_Avoid_: Configuration copy, credential store, upstream project state

**Upstream Change Information**:
Semantic information supplied with changes so a user's AI can assess their impact before proposing updates to a Consumer Configuration.
_Avoid_: Configuration migration, synchronization state

**Review Cursor**:
The upstream release or commit a user's AI has already reviewed. It records review progress, not synchronization.
_Avoid_: Synchronized version, installed version

**Recovery Path**:
A usable way to restore a Consumer Configuration before an AI changes it, normally provided by version control or a backup of affected files.
_Avoid_: Undo promise, upstream rollback

**Configuration Guidance**:
The fixed workflow for a user's AI: understand the goal, inspect the environment, read relevant modules, propose a plan and impact, obtain confirmation, modify, validate, and preserve user intent.
_Avoid_: Automatic synchronization, configuration installer

**Review Policy**:
The repository-level rules shared by active audits, deterministic local checks, and pull-request AI review.
_Avoid_: Review prompt, CI-only rule

**Configuration Audit**:
A security and usability review in which deterministic checks detect known patterns and AI semantic review evaluates context.
_Avoid_: Formatting check, unaided manual review

**Sensitive Information**:
Secrets or private identifiers that must not enter public Reference Configurations, including credentials, private network details, private email addresses, device identifiers, real home directories, and usernames.
_Avoid_: Maintainer Preference, approved public identity

**Public Identity Exception**:
Maintainer identity information explicitly approved for public configuration through an allowlist.
_Avoid_: Scanner suppression, privacy waiver

**Blocking Finding**:
A secret or privacy risk that prevents a change from being accepted.
_Avoid_: Warning

**Advisory Finding**:
A generality, portability, or documentation concern that a maintainer may accept with a recorded reason.
_Avoid_: Security exception
