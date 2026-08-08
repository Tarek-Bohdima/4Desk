# Tutorial: set up a 4desk dev environment on macOS

By the end you will build and run the 4desk desktop client from source on macOS (Intel or Apple Silicon).

## 1. Install toolchains

```sh
brew install cmake ninja nasm protobuf
# Rust (if missing): https://rustup.rs  •  Flutter (stable channel): https://docs.flutter.dev/get-started
```

## 2. Clone with submodules

```sh
git clone --recurse-submodules https://github.com/Tarek-Bohdima/4desk.git client
cd client
git remote add upstream https://github.com/rustdesk/rustdesk
```

## 3. Native dependencies (vcpkg)

```sh
git clone https://github.com/microsoft/vcpkg ~/vcpkg
~/vcpkg/bootstrap-vcpkg.sh -disableMetrics
export VCPKG_ROOT=~/vcpkg
~/vcpkg/vcpkg install   # manifest mode, reads vcpkg.json — takes a while (aom!)
```

## 4. Generate the Flutter–Rust bridge (once, and after `flutter_ffi.rs` changes)

```sh
cargo install cargo-expand --version 1.0.95 --locked
cargo install flutter_rust_bridge_codegen --version 1.80.1 --features uuid --locked
~/.cargo/bin/flutter_rust_bridge_codegen --rust-input ./src/flutter_ffi.rs \
  --dart-output ./flutter/lib/generated_bridge.dart \
  --c-output ./flutter/macos/Runner/bridge_generated.h
```

## 5. Build and run

```sh
cargo check                      # fast sanity check of the Rust core
cd flutter && flutter pub get && cd ..
python3 build.py --flutter       # desktop app bundle
```

Known macOS gotchas (verified on Intel, Flutter 3.44):
- **NASM 3.x breaks the vcpkg `aom` build** — build NASM 2.16.03 from source and put it first in `PATH` for the `vcpkg install` step.
- **Flutter ≥3.27 API renames**: the committed sources target Flutter 3.24.5. On newer Flutter, apply `.github/patches/apply_flutter_3.44_source_patches.sh` before building (needs GNU sed — `brew install gnu-sed`; do **not** commit the resulting changes).
- **Ad-hoc signature mismatch**: if the built app dies instantly with `Library not loaded: FlutterMacOS...different Team IDs`, re-sign the bundle: `codesign --force --deep -s - <path>/4desk.app`.

The app should launch showing the **4desk** name and register an ID against the trial server (check `docker logs 4desk-hbbs` for `update_pk`). To point a debug build at your own server at build time:

```sh
FOURDESK_ID_SERVER=192.168.1.19 FOURDESK_RS_PUB_KEY="<contents of server data/id_ed25519.pub>" python3 build.py --flutter
```

Next: [run the full stack locally](run-full-stack-locally.md).
