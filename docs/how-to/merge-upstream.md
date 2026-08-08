# How to merge upstream RustDesk updates

Goal: absorb upstream fixes/features while keeping the 4Desk delta intact. Do this at least for every upstream stable release (security fixes!).

## Main repo

```sh
git fetch upstream --tags
git checkout -b merge/upstream-<version> 4desk/main
git merge <version>            # e.g. 1.5.0 — merge release tags, not master tip
```

Conflict rules of thumb:
- `src/lang/*.rs`: always take upstream (we never edit them).
- Brand-touched files (see `docs/explanation/rebrand-surface.md`): re-apply the 4Desk value; the diff is deliberately tiny.
- `src/four_desk/`, `flutter/lib/four_desk/`: ours only, upstream never touches them.

Then run the quality gates (fmt, clippy, dart format, analyze, full tests), smoke-test locally, open a PR with a tracking issue noting the new upstream base version.

## hbb_common submodule

The fork lives at Tarek-Bohdima/4desk-hbb-common (branch `4desk/main`, remotes: `origin` = rustdesk/hbb_common, `fork` = ours).

```sh
cd libs/hbb_common
git fetch origin
git merge <upstream-commit-matching-the-release>
git push fork 4desk/main
cd ../.. && git add libs/hbb_common   # bump submodule pointer in the same PR
```

## After merging

Update the base-version note in README.md and record the upstream version in the release notes of the next 4Desk release.
