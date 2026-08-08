# Licensing

4Desk is a derivative of RustDesk, licensed **AGPL-3.0** (see `LICENCE`). Consequences:

- Distributing 4Desk binaries (installers, app-store builds, downloads for customers) requires the corresponding source to be publicly available. This repository satisfies that obligation — it must remain public and current with what we ship.
- RustDesk attribution and license notices stay intact.
- AGPL does **not** extend to separate programs the client talks to over the network: the server stack configuration and any private backend services (accounts, billing, garage features) can stay closed. Rule of thumb: in-client code is public; server-side logic is ours alone.
- Secrets (signing keys, server private keys, credentials) never belong in this repo regardless of licensing.
- Apple App Store has known friction with AGPL apps; preferred iOS distribution is TestFlight/business distribution (decide when iOS ships).
