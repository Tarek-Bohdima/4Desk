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

## 4. Build and run

```sh
cargo check                      # fast sanity check of the Rust core
cd flutter && flutter pub get && cd ..
python3 build.py --flutter       # desktop app bundle
```

The app should launch showing the **4desk** name. To point a debug build at your own server at build time:

```sh
FOURDESK_ID_SERVER=192.168.1.19 FOURDESK_RS_PUB_KEY="<contents of server data/id_ed25519.pub>" python3 build.py --flutter
```

Next: [run the full stack locally](run-full-stack-locally.md).
