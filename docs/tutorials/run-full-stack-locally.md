# Tutorial: run the full 4Desk stack locally

You will run the signaling server + admin panel on your machine and connect a locally built client to it. Prerequisite: [dev environment](dev-environment-macos.md), Docker Desktop.

## 1. Start the server stack

In the workspace's `server/` directory:

```sh
cp .env.example .env          # SERVER_ADDR = this machine's LAN IP (ipconfig getifaddr en0)
docker compose up -d
docker logs 4desk-api 2>&1 | grep "Admin Password"
```

Open `http://localhost:21114/_admin/`, log in as `admin` with that password, change it.

## 2. Build a client pointed at your server

```sh
FOURDESK_ID_SERVER=$(ipconfig getifaddr en0) \
FOURDESK_RS_PUB_KEY="$(cat ../server/data/id_ed25519.pub)" \
python3 build.py --flutter
```

(If your LAN IP matches the defaults baked into the fork, plain `python3 build.py --flutter` works.)

## 3. Connect

Launch 4Desk on two machines (or one machine + an Android emulator running the APK). Each client registers an ID with your hbbs; enter one client's ID in the other and connect. In the admin panel you should see both devices under Devices.

Troubleshooting: firewall must allow TCP 21114-21119 and UDP 21116 to the server machine; both clients must use the same key (`server/data/id_ed25519.pub`).
