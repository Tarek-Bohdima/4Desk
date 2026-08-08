# Architecture

## The moving parts

```
4Desk client (this repo)          server stack (workspace ../server, Docker)
┌─────────────────────────┐       ┌─────────┐  ┌─────────┐  ┌──────────────┐
│ Flutter UI (flutter/)   │◄─────►│  hbbs   │  │  hbbr   │  │ rustdesk-api │
│   │ FFI                 │       │ ID/     │  │ relay   │  │ admin panel, │
│ Rust core (src/, libs/) │       │ rendez- │  │ (P2P    │  │ addr books,  │
│  capture·codec·input·net│       │ vous    │  │ fallback)│ │ web client   │
└─────────────────────────┘       └─────────┘  └─────────┘  └──────────────┘
```

- Clients register their ID with **hbbs** (port 21116); connections go peer-to-peer when possible, else through **hbbr** (21117). Both enforce our key (`-k _`).
- **rustdesk-api** (21114) is the community admin layer (lejianwen/rustdesk-api): user accounts, device lists, address books. The client's API server defaults to `http://<id-server>:21114`.
- Server identity/defaults are baked at build time from `libs/hbb_common/src/config.rs`, overridable via `FOURDESK_ID_SERVER` / `FOURDESK_RS_PUB_KEY` env at build.

## Fork strategy

Public fork of rustdesk/rustdesk (AGPL-3.0), base pinned to a stable upstream tag; `upstream` remote for merges. The whole design optimizes for **small delta**: brand identity centralized in the hbb_common fork, all 4Desk features isolated in `src/four_desk/` + `flutter/lib/four_desk/` behind feature flags, upstream files touched only at explicit integration points. Proprietary business logic (garage management, billing, …) must live in private server-side services that the client talks to over the network — never in this repo.

## Why Flutter stays

The product value is in the Rust engine; the UI is upstream's actively developed Flutter app. Rewriting in another toolkit (KMM etc.) would detach us from upstream UI fixes and cost months for zero user value.
