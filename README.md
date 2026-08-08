<h1 align="center">4Desk</h1>

Remote desktop for garages — control shop PCs, diagnostic stations, and tablets from anywhere, on your own self-hosted infrastructure.

4Desk is a fork of [RustDesk](https://github.com/rustdesk/rustdesk) (based on upstream release 1.4.9), rebranded and extended for garage workflows. Enormous credit to the RustDesk authors — the remote-desktop engine (Rust) and UI (Flutter) are their work. Licensed under [AGPL-3.0](LICENCE); the complete source of every distributed 4Desk build lives in this repository.

> [!Caution]
> **Misuse disclaimer:** unauthorized access, control, or invasion of privacy with this software is strictly against our guidelines. The authors are not responsible for misuse of the application.

## Platforms

Windows, macOS, Linux, Android (phones/tablets); iOS/iPadOS and web planned.

## Documentation ([Diátaxis](https://diataxis.fr/))

- **Tutorials** — [dev environment & running the full stack locally](docs/tutorials/)
- **How-to guides** — [merge upstream updates, cut a release](docs/how-to/)
- **Reference** — [brand constants & build matrix](docs/reference/)
- **Explanation** — [architecture, rebrand surface, licensing](docs/explanation/)

## Repository layout

- Rust core: `src/`, `libs/` (screen capture, input, codecs, networking). `libs/hbb_common` is a forked submodule carrying 4Desk identity and server defaults.
- Flutter UI: `flutter/` (desktop + mobile). 4desk-specific code is isolated in `src/four_desk/` and `flutter/lib/four_desk/`, feature-flagged.
- The server stack (hbbs/hbbr + admin panel) lives in the workspace's sibling `server/` directory, not in this repo.

## Contributing

Every PR must link a tracking issue with acceptance criteria. TDD is mandatory; existing tests are never edited to make them pass. CI gates: `cargo fmt`/`clippy`, `dart format`/`flutter analyze`, full test suite. See [CLAUDE.md](CLAUDE.md).
