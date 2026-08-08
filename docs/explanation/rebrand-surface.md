# Rebrand surface: RustDesk → 4desk

**Explanation (Diátaxis).** Maps every branding touch point in the codebase (audited at upstream tag 1.4.9) and the mechanism used to change it. Governing principle: smallest possible diff against upstream so `git merge upstream/master` stays cheap.

## The one lever that does most of the work

The runtime app name lives in `config::APP_NAME` (`libs/hbb_common/src/config.rs` — a **separate submodule repo**, so it needs its own fork). Everything downstream derives from it via `get_app_name()` (`src/common.rs:1003`):

- **All UI strings/translations**: `src/lang.rs:226-245` replaces the literal "RustDesk" in every translation with `get_app_name()` at lookup time. The ~40 `src/lang/*.rs` files (1107 occurrences) need **zero edits**.
- **URI scheme**: derived — `get_uri_prefix()` = lowercased app name + `://` (`src/common.rs:1012`), so `4desk://` is automatic, including Windows registry protocol registration.
- **Windows service, firewall rules, registry uninstall key, sc stop/delete**: all use `get_app_name()`.
- **macOS bundle/plist/scripts**: `correct_app_name()` (`src/platform/macos.rs:305`) rewrites `com.carriez.rustdesk`/`RustDesk` in all embedded scripts at runtime — `privileges_scripts/*` need no edits.
- **Linux .desktop filename, app-id, service management**: derived (`src/platform/linux.rs:2115`, `:2217`).
- **Dart window titles**: `bind.mainGetAppNameSync()` — already dynamic.

Also in `hbb_common/src/config.rs`: `ORG` (macOS bundle prefix), `RENDEZVOUS_SERVERS`, `RS_PUB_KEY`, `PROD_RENDEZVOUS_SERVER`, config-dir/`RustDesk2.toml` naming.

**Decision: fork hbb_common** (as `4desk-hbb-common`), set `APP_NAME = "4desk"`, `ORG`, and our server/key defaults there; point `.gitmodules` at the fork. This beats the alternative (RustDesk's signed `custom.txt` mechanism, `src/common.rs:2083-2249`) because that blob is verified against RustDesk's hardcoded pubkey (`src/common.rs:2185`) — usable only via a 1-line key swap plus our own signing pipeline; more moving parts for the same result. We may adopt it later for per-customer config.

## Deliberate side effect

With `APP_NAME != "RustDesk"`, `is_rustdesk()` (`src/common.rs:1009`) turns false and `is_custom_client()` (`src/common.rs:2284`) turns true → upstream update checks and rustdesk.com-specific paths disable themselves. This is desired for 4desk; revisit if any gated feature is missed.

## Unavoidable source edits (small, enumerable)

Rust side:
- `src/common.rs:1083` hardcoded fallback `https://admin.rustdesk.com` (api server); `is_public()` `rustdesk.com` match `:1086`.
- Windows: new Inno GUID `src/platform/windows.rs:1275`; custom-client staging dir `:1990`; self-update file globs `:3749`; msgbox caption `:3816`.
- Whiteboard window titles: `src/whiteboard/{linux.rs:216,macos.rs:85,windows.rs:29}`.
- Updater filenames `src/updater.rs:146,153`; docs URLs `src/client.rs:132,3334`.
- Windows portable packer: `libs/portable/src/main.rs:20` `APP_PREFIX`, `bin_reader.rs:76,82`, `generate.py`.
- `Cargo.toml:6` description only. **Keep crate name `rustdesk` and lib `librustdesk`** — renaming ripples through CMake/runners/imports for zero user-visible benefit.

Flutter/platform manifests:
- Android: `applicationId` in `flutter/android/app/build.gradle:100`, manifest labels (`AndroidManifest.xml:28,49` → point at `res/values/strings.xml`), Kotlin literals in `MainService.kt`/`FloatingWindowService.kt`/`BootReceiver.kt`. **Keep Kotlin package path `com.carriez.flutter_hbb`** (changing applicationId does not require moving package dirs).
- iOS: bundle id in `Runner.xcodeproj/project.pbxproj` (3 sites), `Info.plist` display name (deferred with iOS).
- macOS: `flutter/macos/Runner/Configs/AppInfo.xcconfig:8,11` (PRODUCT_NAME, bundle id) — the single macOS lever; `Info.plist:29,32` URL scheme.
- Windows: `flutter/windows/CMakeLists.txt:3,7` BINARY_NAME, `runner/Runner.rc:93-98`, `main.cpp:66` fallback title.
- Linux: `flutter/linux/CMakeLists.txt:7,10`, `my_application.cc:119,145,149` (leave channel names `org.rustdesk.rustdesk/*` — wire identifiers, must match Dart).
- Dart: one literal at `flutter/lib/desktop/widgets/tabbar_widget.dart:644`; web stub `flutter/lib/web/bridge.dart:1611`. Leave identifiers (`kPlatformAdditionsRustDeskVirtualDisplays`, `RustDeskMultiWindowManager`, IDD driver names) — protocol/driver identity, not brand.
- `flutter/pubspec.yaml:1` `name: flutter_hbb` — **do not rename** (every import ripples).

## Assets

Replace `res/icon.png` + `res/mac-icon.png`, rerun `flutter_launcher_icons` (config in `flutter/pubspec.yaml:127-141`) → regenerates Android/iOS/Windows/macOS/web icons. Manual extras: `res/*.ico` (`res/gen_icon.sh`), tray icons, `res/logo*.svg`, `flutter/assets/icon.svg`, Android notification icon `ic_stat_logo`, fastlane store images.

## Packaging & CI

- MSI already parametrized: pass `--app-name 4desk` to `res/msi/preprocess.py` (no source edits).
- `build.py:17` `hbb_name` + hardcoded deb/dmg/portable paths — edit once.
- Static Linux assets renamed + edited: `res/rustdesk{,-link}.desktop`, `res/rustdesk.service`, `res/pam.d/`, `res/PKGBUILD`, `res/rpm*.spec`, `res/DEBIAN/*`.
- AppImage `appimage/AppImageBuilder-*.yml:5-22`; Flatpak `flatpak/rustdesk.json` + `com.rustdesk.RustDesk.metainfo.xml` (rename file to new app-id).
- CI: `.github/workflows/flutter-build.yml` hardcodes `rustdesk-${VERSION}-…` in ~40 artifact lines; minimal-diff approach = introduce `PKG_NAME` env at the top and substitute. Callers: `flutter-tag.yml` (releases), `flutter-nightly.yml`, `flutter-ci.yml`. Keep third-party `rustdesk-org/*` action references pointing upstream.

## Execution order (Phase 2)

1. Fork + edit hbb_common (APP_NAME/ORG/server defaults), repoint `.gitmodules`.
2. Rust edits listed above.
3. Platform manifests (Android/macOS/Windows/Linux; iOS deferred).
4. Assets once the 4desk logo exists.
5. `build.py`/`res/` packaging + CI `PKG_NAME` overlay.
6. Verify: macOS build shows 4desk branding and connects to the trial server.
