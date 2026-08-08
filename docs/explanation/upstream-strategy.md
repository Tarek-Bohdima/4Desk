# Upstream strategy: staying mergeable after the rebrand

**Explanation (Diátaxis).** Why the fork tracks upstream the way it does, and where merge conflicts can and cannot happen. The operational steps live in [how-to/merge-upstream.md](../how-to/merge-upstream.md).

## "Behind master" is by design

GitHub shows `4desk/main` as N commits behind `rustdesk/rustdesk:master`. That is intentional: we base on upstream **release tags** (currently 1.4.9), never on master's tip, because master carries unreleased and unstabilized work. The counter grows between upstream releases and resets (conceptually) each time we merge the next tag. Merge every upstream release promptly — small, regular merges are the whole game; letting drift accumulate is what makes forks die.

## Conflict-surface map

The rebrand was engineered so that upstream churn lands almost entirely in code we never modified:

| Zone | Conflict risk | Why |
|---|---|---|
| `src/lang/*.rs` translations (1100+ "RustDesk" strings) | **None** | Untouched — `src/lang.rs` substitutes the app name at runtime |
| Code deriving from `get_app_name()` (services, registry, URI scheme, titles, macOS scripts) | **None** | One constant drives it; upstream logic changes merge cleanly |
| `src/four_desk/`, `flutter/lib/four_desk/`, `4desk-*.yml`, docs | **None** | Files upstream doesn't have |
| `libs/hbb_common` fork | **Low** | 3 constants in one file; merged separately, submodule pointer bumped |
| Point edits (Inno GUID, whiteboard titles, updater filenames, Android labels, macOS xcconfig) | **Low** | One-line diffs; conflict only if upstream edits the same line |
| `flutter-build.yml`, `build.py`, renamed `res/` packaging files | **Moderate** | Mechanical `rustdesk-` → `4desk-` renames across many lines that upstream also edits |

**Resolution rule for the moderate zone:** take upstream's structure, re-apply the 4desk name. Never fight upstream's refactors — the rename is mechanical and can always be re-run.

Realistic cost per upstream release: minutes to an hour, mostly in packaging/CI files, verified by the quality gates plus a local smoke test.

## The two habits that keep merges cheap

1. Merge upstream **release tags** promptly (one issue-tracked PR per release, upstream base recorded in release notes).
2. Never scatter 4desk changes through upstream files — new code goes in `four_desk/` modules behind feature flags, touching upstream only at single-line integration points.
