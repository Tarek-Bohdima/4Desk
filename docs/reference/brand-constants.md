# Reference: brand constants & identifiers

| Item | Value | Where |
|---|---|---|
| App name | `4Desk` | `libs/hbb_common/src/config.rs` `APP_NAME` (fork) |
| macOS org prefix | `com.fourdesk` | hbb_common `ORG` |
| Bundle/application id (Android, macOS, Linux) | `com.fourdesk.app` | `flutter/android/app/build.gradle`, `flutter/macos/Runner/Configs/AppInfo.xcconfig`, `flutter/linux/CMakeLists.txt` |
| URI scheme | `4desk://` | derived from app name (`get_uri_prefix()`) |
| Binary name | `4Desk` (`[[bin]]` in `Cargo.toml`); lib stays `librustdesk` | `Cargo.toml`, Flutter runner CMake |
| Default ID server | `192.168.1.19` (trial) — override `FOURDESK_ID_SERVER` | hbb_common `RENDEZVOUS_SERVERS` |
| Server public key | trial key — override `FOURDESK_RS_PUB_KEY` | hbb_common `RS_PUB_KEY` |
| Windows installer GUID | `{D5E41269-54AB-44A5-9D39-DC0ADA85C049}_is1` | `src/platform/windows.rs` |
| Portable packer magic | `fourdesk` (8 bytes exactly) | `libs/portable/src/bin_reader.rs`, `generate.py` |
| Flatpak app id | `com.fourdesk.app` | `flatpak/4desk.json` |
| MSI branding | pass `--app-name 4Desk` | `res/msi/preprocess.py` |

**Never rename** (wire/protocol/upstream identity): crate `rustdesk`, lib `librustdesk`, Flutter package `flutter_hbb`, Kotlin package `com.carriez.flutter_hbb`, Linux channels `org.rustdesk.rustdesk/*`, `kPlatformAdditionsRustDesk*` keys, IDD driver names, `rustdesk-org/*` CI action references.

Ports: 21114 API · 21115-21116(+udp) hbbs · 21117/21119 hbbr · 21118 web socket.
