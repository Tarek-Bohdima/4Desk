# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

4Desk: a rebranded fork of RustDesk (base: upstream tag 1.4.9) — remote desktop for automotive workshops. Rust core + Flutter UI over FFI. `libs/hbb_common` is a **forked submodule** (Tarek-Bohdima/4Desk-hbb-common, branch `main`) holding `APP_NAME`, `ORG`, and default server/key. AGPL-3.0: this repo stays public; proprietary logic belongs in private server-side services, never here. The server stack lives in the workspace sibling `../server/` (see the workspace-root CLAUDE.md).

## Hard rules (user-mandated, non-negotiable)

1. **TDD**: write the failing test first. **Never modify existing unit/instrumentation/E2E tests to make them pass** — fix the code; changing test expectations requires Tarek's explicit sign-off. Goldens count as tests: update only via a deliberate `--update-goldens` commit.
2. **Every PR links a tracking issue** (`Closes #N`) with acceptance criteria, created before the PR. Use `-R Tarek-Bohdima/4Desk` with `gh` (a fork otherwise defaults to upstream). PRs/issues closed for non-obvious reasons get an explanatory comment.
3. **Minimal upstream diff**: new 4Desk code lives in `src/four_desk/` and `flutter/lib/four_desk/`, touching upstream files only at small integration points, behind feature flags (`docs/how-to/add-a-feature-flag.md`). Cheap upstream merges are a top priority.
4. **Merge policy** (`docs/how-to/merge-policy.md`): upstream-sync PRs use a **merge commit** (never squash — it breaks shared ancestry and every future merge); all other PRs are **squashed**. Prefer independent PRs off `main`; GitHub stacks only for genuinely dependent work (stacked PRs merge via `gh api -X PUT .../pulls/N/merge-async`). Branches auto-delete on merge; also delete local copies.
5. Every `four_desk` widget ships with a **golden test** (`matchesGoldenFile`).

## Commands

- Rust: `cargo check`, `cargo test four_desk --lib` (our tests; full `cargo test` for everything). Needs `VCPKG_ROOT=~/vcpkg`; native deps: `~/vcpkg/vcpkg install` from repo root (manifest mode). macOS: NASM 3.x breaks the aom build — put NASM 2.16.03 first in PATH (`~/.local/nasm216/bin`).
- Flutter: `cd flutter && flutter pub get`; tests `flutter test test/four_desk`; format/lint `dart format lib/four_desk test/four_desk` + `dart analyze lib/four_desk` (not `flutter analyze` — it compiles the whole package and needs the generated bridge).
- Bridge codegen (before first desktop build, and after `src/flutter_ffi.rs` changes): `flutter_rust_bridge_codegen --rust-input ./src/flutter_ffi.rs --dart-output ./flutter/lib/generated_bridge.dart --c-output ./flutter/macos/Runner/bridge_generated.h` (install: `cargo install flutter_rust_bridge_codegen --version 1.80.1 --features uuid --locked` + `cargo-expand 1.0.95`).
- Desktop build: `python3 build.py --flutter`. Committed sources target **Flutter 3.24.5**; on Flutter ≥3.27 apply `.github/patches/apply_flutter_3.44_source_patches.sh` first (needs GNU sed; never commit its changes). If the built macOS app dies with a FlutterMacOS Team-ID error: `codesign --force --deep -s - <path>/4Desk.app`.
- Point a build at a server: `FOURDESK_ID_SERVER=<host> FOURDESK_RS_PUB_KEY=<key> python3 build.py --flutter`.
- hbb_common submodule check: `cd libs/hbb_common && cargo check` (its fork remote is named `fork`; `origin` is upstream rustdesk/hbb_common).

## CI (4desk-ci.yml — required checks `rust-gates`, `flutter-gates`)

Runs on every PR (any base — stacked PRs need reporting checks) and pushes to `main`. Doc-only changes (`docs/**`, `*.md`) skip the gates via the `changes` paths-filter job — never use `paths-ignore` on required checks (doc PRs would hang). Branch protection is strict: refresh the branch on latest `main` before merge (merge main in for plain PRs; rebase inside stacks). Inherited upstream workflows (`ci.yml`, `flutter-ci.yml`, nightly, fdroid) are `workflow_dispatch`-only — keep them that way. Releases: push tag `v0.X.Y` → `4desk-release.yml` (see `docs/how-to/cut-a-release.md`).

## Branding rules

Display brand is **4Desk** (capital D); technical identifiers stay lowercase: binary `[[bin]] name = "4desk"`, URI scheme `4desk://` (derived, auto-lowercased), bundle id `com.fourdesk.app`, artifact names `4desk-*`. Runtime name comes from `config::APP_NAME` (hbb_common) via `get_app_name()`; translations auto-substitute "RustDesk" at lookup (`src/lang.rs`) — **never edit `src/lang/*.rs`**. Keep untouched: crate `rustdesk`, lib `librustdesk`, Flutter package `flutter_hbb`, Kotlin package path `com.carriez.flutter_hbb`, Linux channels `org.rustdesk.rustdesk/*`, wire-protocol identifiers, `rustdesk-org/*` CI action refs. Full map: `docs/explanation/rebrand-surface.md`; values: `docs/reference/brand-constants.md`.

## Upstream merges

Merge upstream **release tags** promptly, never master tip ("behind master" on GitHub is by design). `git fetch upstream && git merge <tag>` on a branch off `main`; conflict rules and the hbb_common submodule dance: `docs/how-to/merge-upstream.md`; rationale and conflict-surface map: `docs/explanation/upstream-strategy.md`.
