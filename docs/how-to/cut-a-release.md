# How to cut a 4Desk release

Versioning: 4Desk uses its own SemVer (`v0.1.0`, `v0.2.0`, …), independent of the upstream RustDesk base. Always record the upstream base version in the release notes.

1. **Sync**: optionally [merge the latest upstream release](merge-upstream.md) first — never release with unreviewed upstream changes.
2. **Bump versions** in one PR (issue-tracked): `Cargo.toml` `version`, `flutter/pubspec.yaml` `version`, `VERSION` env in `.github/workflows/flutter-build.yml`.
3. **Gates**: CI green on `4desk/main`; run `/security-review` on the release diff.
4. **Smoke test** locally: macOS build connects to the trial server; one remote-control session works.
5. **Tag**: `git tag v0.X.Y && git push origin v0.X.Y` — `4desk-release.yml` builds all platforms and publishes artifacts (`4desk-<version>-<platform>`) to the GitHub Release for that tag.
6. **Release notes**: what changed, upstream base version, known issues.

Signing status: Windows/macOS/Android builds are **unsigned** until certificates exist (`ANDROID_SIGNING_KEY`, `MACOS_P12_*`, `SIGN_*` secrets) — fine for the trial, required before customer distribution. iOS deferred entirely.
