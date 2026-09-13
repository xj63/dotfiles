# Releasing

Release only from a clean branch created from current `main`. Read `[Unreleased]`, confirm every user-affecting entry names an application or repository scope, supplies a category, explains impact, and includes migration guidance when relevant. Classify the largest included change with `scripts/release-check classify <change-kind>`; breaking protocol or module-layout changes are major, modules/capabilities/dependencies/behavior are minor, and documentation or non-behavioral corrections are patch.

Prepare one pull request that leaves a fresh empty `[Unreleased]`, moves the complete batch under `## [X.Y.Z] - YYYY-MM-DD`, and adds `docs/releases/X.Y.Z.md` with an H1 followed by the exact release body. Run:

```sh
python3 -m unittest discover -s tests -v
scripts/check all
scripts/release-check verify X.Y.Z --notes docs/releases/X.Y.Z.md
```

Complete the local Configuration Audit and record it on the PR. Merge only after the protected deterministic check passes. Semantic review remains the recorded local audit; GitHub requires no AI credential.

On the updated clean `main`, verify the merge commit and create the matching annotated tag. Validate the local tag before making any remote change. Push it only after validation, then create the GitHub Release using notes read from the tag rather than the working tree:

```sh
git tag --annotate vX.Y.Z --message "vX.Y.Z"
scripts/release-check verify X.Y.Z --notes docs/releases/X.Y.Z.md --tag-required
git push origin vX.Y.Z
scripts/publish-release X.Y.Z
```

`scripts/publish-release` repeats local tag verification and reads the notes from the tagged tree before invoking GitHub. If either local step fails, it does not call `gh`.

Confirm the GitHub Release targets the same commit as the tag and its body matches the committed notes. A fresh consumer may record the tag as its initial Review Cursor. An existing consumer runs the selected module's update assessment from its earlier cursor; release publication never synchronizes its configuration.
