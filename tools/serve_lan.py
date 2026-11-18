"""Preview the blog on phones in the same Wi-Fi/LAN.

    python tools/serve_lan.py            # drafts hidden
    python tools/serve_lan.py -D         # extra args go to `hugo server`

Finds this computer's LAN address, then runs `hugo server` listening on all interfaces with
that address as baseURL, so links and live reload work from a phone. Open the printed address
on the computer and press the "手机阅读 / Phone" button (bottom right) to get a QR code.

The first run may make Windows ask whether Hugo may accept connections on private networks;
allow it there (private networks only) or the phone can't connect.
"""
import glob
import os
import shutil
import socket
import subprocess
import sys

PORT = int(os.environ.get("PORT", "1313"))


def lan_ip():
    # A UDP "connect" picks the outgoing interface without sending any packet.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def find_hugo():
    """$HUGO, then PATH, then winget's package folder (winget doesn't always link it onto PATH)."""
    if os.environ.get("HUGO"):
        return os.environ["HUGO"]
    found = shutil.which("hugo")
    if found:
        return found
    pkgs = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
    for exe in sorted(glob.glob(os.path.join(pkgs, "Hugo.Hugo.Extended_*", "hugo.exe")) +
                      glob.glob(os.path.join(pkgs, "Hugo.Hugo_*", "hugo.exe"))):
        return exe
    return None


def main():
    hugo = find_hugo()
    if not hugo:
        sys.exit("hugo not found: put it on PATH or set HUGO=<path to hugo>")
    ip = lan_ip()
    url = f"http://{ip}:{PORT}/"
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"\n  Open on this computer: {url}\n  then use the Phone button (bottom right) to scan it.\n", flush=True)
    cmd = [hugo, "server", "-s", root, "--bind", "0.0.0.0", "--port", str(PORT),
           "--baseURL", url, "--appendPort=false", *sys.argv[1:]]
    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
