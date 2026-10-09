import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

SHARED_DRIVE = "mktg,team_drive=0AJ_tFpZKdJ0FUk9PVA:"


def folder_name(name):
    return re.sub(r"\s+", " ", re.sub(r'[\\/:*?"<>|]', " ", name)).strip() + " clips"


def rclone(*args):
    result = subprocess.run(["rclone", *args], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        sys.exit("rclone " + args[0] + " failed:\n" + result.stderr.strip())
    return result.stdout.strip()


def opens_signed_out(link):
    request = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return "accounts.google.com" not in response.url and ".mp4" in response.read().decode("utf-8", "ignore")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        sys.exit("usage: to_drive.py <workdir> [creator or brand name]")
    if not shutil.which("rclone"):
        sys.exit("rclone is not installed")
    workdir = Path(sys.argv[1]).expanduser()
    info = json.loads((workdir / "source-audio.info.json").read_text(encoding="utf-8"))
    remote = SHARED_DRIVE + "Clips/" + folder_name(sys.argv[2] if len(sys.argv) > 2 else info["title"])
    rclone("copy", str(workdir / "clips"), remote, "--include", "*.mp4")
    link = rclone("link", remote).splitlines()[-1]
    print(json.dumps({
        "folder": remote.split(":", 1)[1],
        "uploaded": rclone("lsf", remote).splitlines(),
        "opens_signed_out": opens_signed_out(link),
        "channel": info.get("channel"),
        "youtube": info.get("uploader_url") or info.get("channel_url"),
        "drive": link,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        assert folder_name("A Day | Ironman Prep: Ep. 2") == "A Day Ironman Prep Ep. 2 clips"
        assert folder_name("Ved Iyer") == "Ved Iyer clips"
        print("ok")
    else:
        main()
