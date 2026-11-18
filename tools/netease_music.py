"""Fetch NetEase Cloud Music song details for the {{< music >}} shortcode.

    python tools/netease_music.py 1402719608 1847289377     # add/refresh these songs
    python tools/netease_music.py --all                     # refresh every song in data/music.toml

Writes data/music.toml: title, artist, cover and (if any) LRC lyrics per song id. The audio itself
is not downloaded: the player streams NetEase's own outer link (music.163.com/song/media/outer/url),
which works for songs that are free to play. Edit the file by hand to override any field.
"""
import json
import pathlib
import re
import sys
import time
import tomllib
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "music.toml"
UA = {"User-Agent": "Mozilla/5.0 (blog music metadata)", "Referer": "https://music.163.com/"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        return json.load(r)


def details(ids):
    q = urllib.parse.quote(json.dumps([int(i) for i in ids], separators=(",", ":")))
    songs = get(f"https://music.163.com/api/song/detail/?ids={q}").get("songs") or []
    out = {}
    for s in songs:
        cover = (s.get("album") or {}).get("picUrl") or ""
        out[str(s["id"])] = {
            "title": s.get("name", ""),
            "artist": " / ".join(a.get("name", "") for a in s.get("artists") or []),
            "album": (s.get("album") or {}).get("name", ""),
            "cover": cover.replace("http://", "https://") + ("?param=300y300" if cover else ""),
        }
    return out


def lyric(song_id):
    d = get(f"https://music.163.com/api/song/lyric?id={song_id}&lv=1")
    if d.get("pureMusic") or d.get("nolyric"):
        return ""
    lrc = ((d.get("lrc") or {}).get("lyric") or "").strip()
    # Instrumentals come back as untimed credits plus "纯音乐，暂无歌词": not worth a lyrics pane.
    if "纯音乐" in lrc or not re.search(r"^\[\d+:\d+", lrc, re.M):
        return ""
    return lrc


def toml_str(s):
    if "\n" in s:
        return "'''\n" + s.replace("'''", "’’’") + "\n'''"
    return json.dumps(s, ensure_ascii=False)


def main():
    args = sys.argv[1:]
    current = tomllib.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    ids = list(current) if args == ["--all"] else [a.strip(",") for a in args if a.strip(",").isdigit()]
    if not ids:
        sys.exit(__doc__)
    found = details(ids)
    for i in ids:
        if i not in found:
            print(f"  {i}: not found on NetEase, skipped")
            continue
        time.sleep(0.5)
        found[i]["lrc"] = lyric(i)
        current[i] = {**current.get(i, {}), **found[i]}
        print(f"  {i}: {found[i]['title']} - {found[i]['artist']}{' (lyrics)' if found[i]['lrc'] else ''}")
    lines = ["# NetEase Cloud Music songs for {{< music >}}; written by tools/netease_music.py, safe to edit.", ""]
    for i, song in current.items():
        lines.append(f'["{i}"]')
        for k in ("title", "artist", "album", "cover", "lrc"):
            if song.get(k):
                lines.append(f"{k} = {toml_str(song[k])}")
        lines.append("")
    DATA.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"wrote {DATA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
