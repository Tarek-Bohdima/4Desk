# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

4desk: a rebranded fork of RustDesk (base: upstream tag 1.4.9) — remote desktop for garages. Rust core + Flutter UI. `libs/hbb_common` is a **forked submodule** (Tarek-Bohdima/4desk-hbb-common, branch `4desk/main`) holding `APP_NAME`, `ORG`, and default server/key. AGPL-3.0: this repo stays public; proprietary logic belongs in private server-side services, never here.

## Hard rules (user-mandated, non-negotiable)

1. **TDD**: write the failing test first. **Never modify existing unit/instrumentation/E2E tests to make them pass** — fix the code; changing test expectations requires Tarek's explicit sign-off.
2. **Every PR links a tracking issue** (`Closes #N`) with acceptance criteria. Create the issue before the PR. Use `-R Tarek-Bohdima/4desk` with `gh` (fork defaults to upstream otherwise).
3. **Minimal upstream diff**: new 4desk code lives in `src/four_desk/` and `flutter/lib/four_desk/`, touching upstream files only at small integration points, behind feature flags. Cheap `git merge upstream/master` is a top priority.
4. Quality gates before merge: `cargo fmt --check`, `cargo clippy -- -D warnings`, `dart format --set-exit-if-changed .`, `flutter analyze`, full tests.

## Commands

- Rust check/test: `cargo check`, `cargo test` (needs `VCPKG_ROOT=~/vcpkg`; native deps via `vcpkg install` from repo root, manifest mode)
- Flutter: `cd flutter && flutter pub get && flutter run` (desktop debug), `flutter test`
- Desktop debug build: `python3 build.py --flutter` (see `build.py --help`)
- hbb_common submodule check: `cd libs/hbb_common && cargo check`
- Server stack (workspace sibling `../server/`): `docker compose up -d`; admin panel http://localhost:21114/_admin/
- Build-time server override: `FOURDESK_ID_SERVER=host FOURDESK_RS_PUB_KEY=key cargo build`

## Branding rules

Runtime name comes from `config::APP_NAME` (hbb_common) via `get_app_name()`; translations auto-substitute "RustDesk" at lookup (`src/lang.rs`) — **never edit `src/lang/*.rs`**. Keep untouched: crate name `rustdesk`, lib `librustdesk`, Flutter package `flutter_hbb`, Kotlin package path `com.carriez.flutter_hbb`, Linux channel names `org.rustdesk.rustdesk/*`, wire-protocol identifiers (`kPlatformAdditionsRustDesk*`, IDD driver names). Binary is renamed via `[[bin]] name = "4desk"` in Cargo.toml. Full map: `docs/explanation/rebrand-surface.md`.

## Upstream merges

`git fetch upstream && git merge <upstream-tag>` into a branch off `4desk/main`; resolve, run gates, PR. hbb_common fork merges upstream separately, then bump the submodule pointer. See `docs/how-to/merge-upstream.md`.
